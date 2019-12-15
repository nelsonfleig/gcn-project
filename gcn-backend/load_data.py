# Load the data
from neo4j import GraphDatabase
import networkx as nx

uri = "bolt://ea085e03.databases.neo4j.io:7687"
driver = GraphDatabase.driver(uri, auth=("nelson", "Chichapi198"))

edges = []

def get_edge_pairs(tx):
  for record in tx.run("MATCH (a1:Artist)-[:PLAYED_WITH]->(a2:Artist) RETURN DISTINCT a1.mbid, a2.mbid ORDER BY a1.mbid, a2.mbid"):
    edges.append(tuple((record["a1.mbid"], record["a2.mbid"])))

with driver.session() as session:
  session.read_transaction(get_edge_pairs)



g = nx.Graph()
g.add_edges_from(edges)
nodes_sorted = sorted(list(g.nodes()))

#adj = nx.to_numpy_matrix(g, nodelist=order)
adj = nx.adjacency_matrix(g, nodelist=nodes_sorted) # needed because mask_test_edges requires a rank 1 matrix

print("{} nodes and {} edges loaded successfully from Neo4J to Networkx".format(g.number_of_nodes(), g.number_of_edges()))