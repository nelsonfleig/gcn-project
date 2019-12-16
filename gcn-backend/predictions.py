import numpy as np

from scipy.special import expit

# DB settings
from neo4j import GraphDatabase

uri = "bolt://ea085e03.databases.neo4j.io:7687"
driver = GraphDatabase.driver(uri, auth=("nelson", "Chichapi198"))

# Load adjacency and prediction matrices
nodes_sorted = np.load("nodes_sorted.npy").tolist()
adj_orig = np.load("adj_orig.npy")
adj_pred = np.load("pred_matrix.npy")

def get_predictions_for(mbid, num_predictions=10):

  artist_index = nodes_sorted.index(mbid) # Returns 4250
  #adj_pred = adj_pred.reshape((len(nodes_sorted), -1))

  prediction_probs = []
  for i in range(adj_pred.shape[0]):
    pred = expit(adj_pred[artist_index, i])
    prediction_probs.append(pred)

  prediction_probs = np.array(prediction_probs)
  best_indexes = np.argsort(-prediction_probs)

  # converts ith row of adjacency matrix to a label row
  labels = adj_orig[artist_index].tolist()

  # Collect indices of existing links 
  existing_links = []

  for i in range(len(labels)):
    if labels[i] == 1:
      existing_links.append(i)

  # Collect possible link predictions where the index is not from artist itself or from existing links
  link_predictions = []

  for index in best_indexes:
    if index != artist_index and index not in existing_links:
      link_predictions.append(index)

  # Extract from list the defined number of predictions
  best_predictions_indexes = link_predictions[:num_predictions]

  # Create empty list to populate with top prediction mbids
  best_predictions_mbids = []

  # Associate node index to its mbid
  for i in link_predictions[:num_predictions]:
    best_predictions_mbids.append(nodes_sorted[i])
  
  # Convert mbids to artist names
  #artist_name_predictions = get_names_from_mbids(best_predictions_mbids)

  return best_predictions_mbids

