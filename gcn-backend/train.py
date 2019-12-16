from gcn_model import *

import tensorflow as tf
import time

# Calculates Average Precision and Area Under Curve
def get_roc_score(edges_pos, edges_neg):
    # Since we are using the embeddings in a test scenario, recalculate them with no dropout. 
    feed_dict.update({placeholders['dropout']: 0})
    emb = sess.run(model.embeddings, feed_dict=feed_dict)
       
    # Since we are using the embeddings in a test scenario, recalculate them with no dropout.
    feed_dict.update({placeholders['dropout']: 0})
    emb = sess.run(model.embeddings, feed_dict=feed_dict)
    
    # Predict on test set of positive edges
    preds = InnerProductDecoder.predict_using_embeddings(emb, edges_pos)
    
    # Predict on test set of negative edges
    preds_neg = InnerProductDecoder.predict_using_embeddings(emb, edges_neg)

    # Stack positive/negative predictions and labels 
    preds_all = np.hstack([preds, preds_neg])
    labels_all = np.hstack([np.ones(len(preds)), np.zeros(len(preds_neg))])
    
    # Calculate scores
    roc_score = roc_auc_score(labels_all, preds_all)
    ap_score = average_precision_score(labels_all, preds_all)

    return roc_score, ap_score


def construct_feed_dict(adj_normalized, adj, features, placeholders):
    # construct feed dictionary
    feed_dict = dict()
    feed_dict.update({placeholders['features']: features})
    feed_dict.update({placeholders['adj']: adj_normalized})
    feed_dict.update({placeholders['adj_orig']: adj})
    return feed_dict

tf.compat.v1.disable_eager_execution()

# Define placeholders
placeholders = {
    'features': tf.compat.v1.sparse_placeholder(tf.float32),
    'adj': tf.compat.v1.sparse_placeholder(tf.float32),
    'adj_orig': tf.compat.v1.sparse_placeholder(tf.float32),
    'dropout': tf.compat.v1.placeholder_with_default(0., shape=())
}

# Create model
model = GCNModelAE(placeholders, num_features, features_nonzero)

# TODO: Paper Link....
pos_weight = float(adj.shape[0] * adj.shape[0] - adj.sum()) / adj.sum()
norm = adj.shape[0] * adj.shape[0] / float((adj.shape[0] * adj.shape[0] - adj.sum()) * 2)

# Optimizer
with tf.name_scope('optimizer'):
    opt = OptimizerAE(preds=model.reconstructions, # Tensor reshaped to vector form (n, -1) 
                      labels=tf.reshape(tf.compat.v1.sparse_tensor_to_dense(placeholders['adj_orig'],
                                                                  validate_indices=False), [-1]),
                      pos_weight=pos_weight,
                      norm=norm)
 
print("Finished creating optimizer")

# Initialize session
print("Start session")
sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())

# Construct feed dictionary
feed_dict = construct_feed_dict(adj_norm, adj_label, features, placeholders)




# Train model

NUM_EPOCHS=1
DROPOUT=0.1

cost_val = []
ap_val = []
auc_score_val = []

print("Epochs: ")
for epoch in range(NUM_EPOCHS):
    t = time.time()
    # Construct feed dictionary
    feed_dict = construct_feed_dict(adj_norm, adj_label, features, placeholders)
    feed_dict.update({placeholders['dropout']: DROPOUT})
    # Run single weight update
    outs = sess.run([opt.opt_op, opt.cost], feed_dict=feed_dict)

    # Compute average loss
    avg_cost = outs[1]
    cost_val.append(avg_cost)

    roc_curr, ap_curr = get_roc_score(val_edges, val_edges_false)
    ap_val.append(ap_curr)
    auc_score_val.append(roc_curr)

    # print("Epoch:", '%04d' % (epoch + 1), 
    #      "train_loss=", "{:.5f}".format(avg_cost),
    #      "val_roc=", "{:.5f}".format(roc_curr[-1]),
    #      "val_ap=", "{:.5f}".format(ap_curr),
    #      "time=", "{:.5f}".format(time.time() - t))
    #if epoch % 40 == 0:
      #print("")
    print(epoch, end =" ")

print('\nOptimization Finished!')
print("Final loss: ", cost_val[-1])

# Test the model
roc_score, ap_score = get_roc_score(test_edges, test_edges_false)
print('Test AUC score: {:.5f}'.format(roc_score))
print('Test AP score: {:.5f}'.format(ap_score))

reco = sess.run(model.reconstructions, feed_dict=feed_dict)
pred_matrix = expit(reco).reshape((adj.shape[0], -1))

# Save the required numpy matrices to disk to be used directly to make predictions
nodes_sorted_name = 'nodes_sorted.npy'
adj_file_name = 'adj_orig.npy'
prediction_filename = 'pred_matrix.npy'

nodes_sorted = np.array(nodes_sorted) # Transform list to numpy array for saving
np.save(nodes_sorted_name, nodes_sorted)
np.save(adj_file_name, adj.todense()) # We use todense() because the original adj was transformed to a CSR matrix (sparse matrix)
np.save(prediction_filename, pred_matrix)

print("Sorted nodes list saved as: {}".format(nodes_sorted_name))
print("Adjacency matrix saved as: {}".format(adj_file_name))
print("Prediction matrix saved as: {}".format(prediction_filename))