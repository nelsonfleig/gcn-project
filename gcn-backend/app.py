import json
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from predictions import get_predictions_for
from neo4j import GraphDatabase

# DB Settings
uri = "bolt://ea085e03.databases.neo4j.io:7687"
driver = GraphDatabase.driver(uri, auth=("nelson", "Chichapi198"))

def getAllArtists(mbid):

    def
    for record in tx.run(cypher_query):
      names.append(record['a.name'])

    with driver.session() as session:
        session.read_transaction(get_names)

    cypher_query = 'MATCH (a:Artist) WHERE a.mbid IN [{}] RETURN a.name'.format(query_params)

app = Flask(__name__)
CORS(app)

# Returns all artists
@app.route('/')
def home():
    with open('artists.json') as json_file:
        data = json.load(json_file)
        return jsonify(data)

@app.rout('/artists')
def allArtists():
    return redirect('/')

# Returns a single artists
@app.route('/artists/<artistId>')
def singleArtist(artistId):
    with open('artists.json') as json_file:
        data = json.load(json_file)
        for artist in data:
            if artist['id'] == int(artistId):
                return jsonify({key: value for (key,value) in artist.items()})
        return jsonify("not found")

# Makes a prediction on a given artist
@app.route('/artists/<artistId>/predictions')
def makePrediction(artistId):
    with open('artists.json') as json_file:
        data = json.load(json_file)
        for artist in data:
            if artist['id'] == int(artistId):
                return jsonify({key: value for (key,value) in artist.items() if key != 'id'},
                                {"artist1": "artist1",
                                "artist2": "artist2",
                                "artist3": "artist3"
                                })
        return jsonify("not found")

if __name__ == "__main__":
    app.run(debug=True)