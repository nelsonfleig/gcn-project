# DB settings
from neo4j import GraphDatabase
from predictions import get_predictions_for

uri = "bolt://ea085e03.databases.neo4j.io:7687"
driver = GraphDatabase.driver(uri, auth=("nelson", "Chichapi198"))

# get artist names from list of mbids
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

def get_all_artists():

    artists = []
    cypher_query = 'MATCH (a:Artist) RETURN a.mbid, a.name, a.country LIMIT 30'

    def queryData(tx):
        for record in tx.run(cypher_query):
            artist = {"mbid": record['a.mbid'],
                      "name": record['a.name'],
                      "country": record['a.country']}
            artists.append(artist)

    with driver.session() as session:
        session.read_transaction(queryData)

    return artists

def get_artist_and_preds(mbid):

    artist = {}
    prediction_mbids = get_predictions_for(mbid)
    cypher_query = 'MATCH (a:Artist) WHERE a.mbid = "{}" RETURN a.mbid, a.name, a.country'.format(mbid)

    def queryData(tx):
        for record in tx.run(cypher_query):
            artist["mbid"] = record['a.mbid']
            artist["name"] = record['a.name']
            artist["country"] = record['a.country']
            artist['predictions'] = get_names_from_mbids(prediction_mbids)

    with driver.session() as session:
        session.read_transaction(queryData)

    return artist

def search_artists(name):
    artists = []
    cypher_query = 'MATCH (a:Artist) WHERE a.name =~ ".*(?i){}.*" RETURN a.mbid, a.name, a.country LIMIT 30'.format(name)

    def queryData(tx):
        for record in tx.run(cypher_query):
            artist = {"mbid": record['a.mbid'],
                      "name": record['a.name'],
                      "country": record['a.country']}
            artists.append(artist)

    with driver.session() as session:
        session.read_transaction(queryData)

    return artists
