import json
from flask import Flask, jsonify, redirect
from flask_cors import CORS

from artist_repo import get_all_artists, get_artist_and_preds, search_artists


app = Flask(__name__)
CORS(app)

# Returns all artists
@app.route('/')
def home():
    artists = get_all_artists()
    return redirect('/artists')

@app.route('/artists')
def all_artists():
    artists = get_all_artists()
    return jsonify(artists)
    

# Returns artist info and predictions
@app.route('/artists/<artistId>')
def single_artist(artistId):
    artist = get_artist_and_preds(artistId)
    return jsonify(artist)

@app.route('/artists/search/<name>')
def search(name):
    artists = search_artists(name)
    return jsonify(artists)

if __name__ == "__main__":
    app.run(debug=True)