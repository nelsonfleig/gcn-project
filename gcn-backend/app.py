import json
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from predictions import get_predictions_for
from neo4j import GraphDatabase

# DB Settings
uri = "bolt://ea085e03.databases.neo4j.io:7687"
driver = GraphDatabase.driver(uri, auth=("nelson", "Chichapi198"))

def getAllArtists():

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

def getPredictionsFor(mbid):

    artist_predictions = {}
    cypher_query = 'MATCH (a:Artist) WHERE a.mbid = "{}" RETURN a.mbid, a.name, a.country LIMIT 30'.format(mbid)
    print(cypher_query)
    def queryData(tx):
        for record in tx.run(cypher_query):
            artist_predictions["mbid"] = record['a.mbid']
            artist_predictions["name"] = record['a.name']
            artist_predictions["country"] = record['a.country']
            artist_predictions['predictions'] = get_predictions_for(record['a.mbid'])

    with driver.session() as session:
        session.read_transaction(queryData)

    return artist_predictions

def getArtistData(mbid):
    artist = {}
    cypher_query = 'MATCH (a:Artist) WHERE a.mbid = "{}" RETURN a.mbid, a.name, a.country'.format(mbid)
    print(cypher_query)
    def queryData(tx):
        for record in tx.run(cypher_query):
            artist["mbid"] = record['a.mbid']
            artist["name"] = record['a.name']
            artist["country"] = record['a.country']

    with driver.session() as session:
        session.read_transaction(queryData)

    return artist

app = Flask(__name__)
CORS(app)

# Returns all artists
@app.route('/')
def home():
    artists = getAllArtists()
    return jsonify(artists)

@app.route('/artists')
def allArtists():
    return redirect('/')

# Returns a single artists
@app.route('/artists/<artistId>')
def singleArtist(artistId):
    data = getArtistData(artistId)
    return jsonify(data)

# Makes a prediction on a given artist
@app.route('/artists/<artistId>/predictions')
def makePrediction(artistId):
    data = getPredictionsFor(artistId)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)