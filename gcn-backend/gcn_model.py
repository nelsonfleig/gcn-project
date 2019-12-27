# Import all the libraries we need
from __future__ import absolute_import, division, print_function, unicode_literals

from load_data import adj, nodes_sorted
from utils import mask_test_edges, preprocess_graph, sparse_to_tuple

import tensorflow as tf
from scipy.special import expit
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
import scipy.sparse as sp
import matplotlib.pyplot as plt 

import collections
from collections import namedtuple
import unittest
import os
import sys
import time

print("TensorFlow version: ", tf.__version__)

# The following function creates a test adj matrix in order calculate the model accuracy (see train.py)
adj_train, train_edges, val_edges, val_edges_false, test_edges, test_edges_false = mask_test_edges(adj)
print("Loaded",adj.shape[0],"nodes")
print("Loaded",adj.sum(),"edges")
print()
print("-- Data format --")
print("Full graph adjacency shape:    ", adj.shape, "\t",             type(adj), "number of indices", len(adj.indices))
print("Training graph adjacency shape:", adj_train.shape, "\t",       type(adj_train), "number of indices", len(adj_train.indices))
print("val_edges:                     ", val_edges.shape, "\t",       type(val_edges))
print("val_edges_false:               ", len(val_edges_false), "\t\t",type(val_edges_false))
print("test_edges:                    ", test_edges.shape,"\t",       type(test_edges))
print("test_edges_false:              ", len(test_edges_false),"\t\t",type(test_edges_false))

# The preprocess_graph method implements graph normalization (see Kipf)
adj_norm = preprocess_graph(adj)

# Since the adj_train matrix was not created with with self loops, we add them now.
adj_label = adj_train + sp.eye(adj_train.shape[0])

# Use sparse_to_tuple to 'unpack' the COO object into edges, normalized adjacency values and normalized adjacency shape
adj_label = sparse_to_tuple(adj_label)

# Record the number of nodes and edges from the full adjacency matrix of the PPI yeast.edges dataset. Used below.
num_nodes = adj.shape[0]

# Simple GCN: no node features (featureless). Substitute the identity matrix for the feature matrix: X = I
# The sparse_to_tuple method 'unpacks' the sparse diagonal matrix into a tuple of node coordinates, values and shape
#
features = sparse_to_tuple(sp.identity(num_nodes)) # dim: # of Nodes * # of Features

# The features[2] dereferences the shape object in the features tuple. features[2][1] dereferences the number of unique nodes that can be neighbors of
# any node in the graph. Since we are using an identity matrix, the num_features is equal to the number of nodes in the graph.
# num_features are used by the GCN model below to define the input dimension size.
num_features = features[2][1]

# features[1] dereferences the data object in the features tuple and then use shape[0] to obtain the number of non-zero entries.
# Since we are using an identity matrix, the features_nonzero is equal to the number of nodes in the graph.
# features_nonzero is used by the dropout_sparse method to apply the dropout regularizer to non-zero features.
features_nonzero = features[1].shape[0]

# Dropout for sparse tensors. Currently fails for very large sparse tensors (>1M elements)
def dropout_sparse(x, keep_prob, num_nonzero_elems):
    noise_shape = [num_nonzero_elems]
    random_tensor = keep_prob
    random_tensor += tf.compat.v1.random_uniform(noise_shape)
    dropout_mask = tf.cast(tf.floor(random_tensor), dtype=tf.bool)
    pre_out = tf.compat.v1.sparse_retain(x, dropout_mask)
    return pre_out * (1./keep_prob)

def weight_variable_glorot(input_dim, output_dim, name=""):
    """Create a weight variable with Glorot & Bengio (AISTATS 2010) initialization.
    """
    init_range = np.sqrt(6.0 / (input_dim + output_dim))
    initial = tf.compat.v1.random_uniform(
        [input_dim, output_dim],
        minval=-init_range,
        maxval=init_range,
        dtype=tf.float32)
    return tf.Variable(initial, name=name)

class GraphConvolutionSparse():
    """Graph convolution layer for sparse inputs."""
    def __init__(self, input_dim, output_dim, adj, features_nonzero, dropout=0., act=tf.nn.relu, **kwargs):
        self.name = self.__class__.__name__.lower()
        self.vars = {}
        with tf.compat.v1.variable_scope(self.name + '_vars'):
            self.vars['weights'] = weight_variable_glorot(input_dim, output_dim, name="weights")
        self.dropout = dropout
        self.adj = adj
        self.act = act
        self.issparse = True
        self.features_nonzero = features_nonzero

    def __call__(self, inputs):
        x = inputs
        x = dropout_sparse(x, 1-self.dropout, self.features_nonzero)
        x = tf.compat.v1.sparse_tensor_dense_matmul(x, self.vars['weights'])
        x = tf.compat.v1.sparse_tensor_dense_matmul(self.adj, x)
        outputs = self.act(x)
        return outputs

    def set_weights(self, weights):
        self.vars['weights'] = weights

class GraphConvolution():
    """Basic graph convolution layer for undirected graph without edge labels."""
    def __init__(self, input_dim, output_dim, adj, dropout=0., act=tf.nn.relu, **kwargs):
        self.name = self.__class__.__name__.lower()
        self.vars = {}
        with tf.compat.v1.variable_scope(self.name + '_vars'):
            self.vars['weights'] = weight_variable_glorot(input_dim, output_dim, name="weights")
        self.dropout = dropout
        self.adj = adj
        self.act = act
        self.issparse = False

    def __call__(self, inputs):
        x = inputs
        x = tf.compat.v1.nn.dropout(x, 1-self.dropout)
        x = tf.matmul(x, self.vars['weights'])
        x = tf.compat.v1.sparse_tensor_dense_matmul(self.adj, x)
        outputs = self.act(x)
        return outputs

    def set_weights(self, weights):
        self.vars['weights'] = weights

# Multiplies the graph embeddings by its own transpose to create the reconstruction matrix (before applying the sigmoid function).
# Output is a flattened vector: (# Nodes^2, 1)
class InnerProductDecoder():
    """Decoder model layer for link prediction."""
    def __init__(self, input_dim, dropout=0., act=tf.nn.sigmoid, **kwargs):
        self.dropout = dropout
        self.act = act

    def __call__(self, inputs):
        inputs = tf.compat.v1.nn.dropout(inputs, 1-self.dropout)
        x = tf.transpose(inputs)
        x = tf.matmul(inputs, x)
        x = tf.reshape(x, [-1])
        outputs = self.act(x)
        return outputs

    @staticmethod
    def predict_using_embeddings(embeddings, edges):
        # Taking the dot product of the (embeddings, embeddings.transpose) calculates the vector similarities between each 
        # pair of nodes.
        # adj_rec: adjacency matrix reconstructed from the node embeddings.
        adj_rec = np.dot(embeddings, embeddings.T)

        # The sigmoid function will take the strength of the node pair (edge) relationship as a scalar value from the reconstructed 
        # adjacency matrix, and return the probability that the edge exists.
        predictions = []
        for e in edges:
            # Note: the expit function is another name for the logistic sigmoid function
            predictions.append(expit(adj_rec[e[0], e[1]]))
        return predictions

HIDDEN1=32
HIDDEN2=16
DROPOUT=0.1

class GCNModelAE():
    def __init__(self, placeholders, num_features, features_nonzero, **kwargs):
        self.name = self.__class__.__name__.lower()
        self.inputs = placeholders['features']
        self.input_dim = num_features
        self.features_nonzero = features_nonzero
        self.adj = placeholders['adj']
        self.dropout = placeholders['dropout']
        self.build()

    def _build(self):
        self.hidden1 = GraphConvolutionSparse(input_dim=self.input_dim,
                                              output_dim=HIDDEN1,
                                              adj=self.adj,
                                              features_nonzero=self.features_nonzero,
                                              act=tf.nn.relu,
                                              dropout=self.dropout)(self.inputs)

        self.embeddings = GraphConvolution(input_dim=HIDDEN1,
                                           output_dim=HIDDEN2,
                                           adj=self.adj,
                                           act=lambda x: x,
                                           dropout=self.dropout)(self.hidden1)

        self.z_mean = self.embeddings

        self.reconstructions = InnerProductDecoder(input_dim=HIDDEN2,
                                      act=lambda x: x)(self.embeddings)

    def build(self):
        """ Wrapper for _build() """
        with tf.compat.v1.variable_scope(self.name):
            self._build()
        variables = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES, scope=self.name)
        self.vars = {var.name: var for var in variables}

LEARNING_RATE=0.1

class OptimizerAE(object):
    def __init__(self, preds, labels, pos_weight, norm):
        preds_sub = preds
        labels_sub = labels

        self.cost = norm * tf.reduce_mean(tf.compat.v1.nn.weighted_cross_entropy_with_logits(logits=preds_sub, labels=labels_sub, pos_weight=pos_weight))
        self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=LEARNING_RATE)  # Adam Optimizer

        self.opt_op = self.optimizer.minimize(self.cost)
        self.grads_vars = self.optimizer.compute_gradients(self.cost)

