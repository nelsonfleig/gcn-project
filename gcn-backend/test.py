from neo4j import GraphDatabase
from predictions import get_predictions_for
# DB Settings
uri = "bolt://ea085e03.databases.neo4j.io:7687"
driver = GraphDatabase.driver(uri, auth=("nelson", "Chichapi198"))

def getAllArtists():

    artists = []
    cypher_query = 'MATCH (a:Artist) RETURN a.mbid, a.name, a.country'

    def queryData(tx):
        for record in tx.run(cypher_query):
            artist = {"mbid": record['a.mbid'],
                      "name": record['a.name'],
                      "country": record['a.country']}
            artists.append(artist)

    with driver.session() as session:
        session.read_transaction(queryData)

    return artists

mbid = '561d854a-6a28-4aa7-8c99-323e6ce46c2a'
def getPredictionsFor(mbid):

    artist = {}
    cypher_query = 'MATCH (a:Artist) WHERE a.mbid = "{}" RETURN a.mbid, a.name, a.country LIMIT 30'.format(mbid)
    print(cypher_query)
    def queryData(tx):
        for record in tx.run(cypher_query):
            artist["mbid"] = record['a.mbid']
            artist["name"] = record['a.name']
            artist["country"] = record['a.country']
            artist['predictions'] = get_predictions_for(record['a.mbid'])

    with driver.session() as session:
        session.read_transaction(queryData)

    return artist

print(getPredictionsFor(mbid))