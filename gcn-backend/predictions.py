import numpy as np
from load_data import nodes_sorted
from scipy.special import expit

# DB settings
from neo4j import GraphDatabase

uri = "bolt://ea085e03.databases.neo4j.io:7687"
driver = GraphDatabase.driver(uri, auth=("nelson", "Chichapi198"))

# Load adjacency and prediction matrices
adj_orig = np.load("adj_orig.npy", allow_pickle=True)
adj_pred = np.load("pred_matrix.npy")

mbid = '561d854a-6a28-4aa7-8c99-323e6ce46c2a' # Miles Davis

def get_predictions_for(mbid):

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

  # makes link predictions if there is no edge exists yet
  existing_links = []

  for i in range(len(labels)):
    if labels[i] == 1:
      existing_links.append(i)

  link_predictions = []

  for index in best_indexes:
    if index != artist_index and index not in existing_links:
      link_predictions.append(index)

  best_3_predictions_indexes = link_predictions[:3]

  best_3_predictions_mbids = []

  NUM_PREDICTIONS = 3

  for i in link_predictions[:3]:
    best_3_predictions_mbids.append(nodes_sorted[i])
  
  artist_name_predictions = get_names_from_mbids(best_3_predictions_mbids)

  return artist_name_predictions

# get artist names from neo4j
def get_names_from_mbids(prediction_mbids):

  names = []
  def get_names(tx):

    query_params = ', '.join(["'{}'".format(c) for c in prediction_mbids])
    cypher_query = 'MATCH (a:Artist) WHERE a.mbid IN [{}] RETURN a.name'.format(query_params)

    for record in tx.run(cypher_query):
      names.append(record['a.name'])

  with driver.session() as session:
        session.read_transaction(get_names)
    
  return names

print(get_predictions_for(mbid))