from flask import Flask, request
from urllib.parse import urlparse
import sys
from pathlib import Path
#Adding our recommend
sys.path.append(str(Path(__file__).parent.parent) + "/recommend-logic")

from recommend import get_recommendations, get_recommendations_by_genre
import json

app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    return app

@app.route('/')
def health_check():
    return {
        "author": "Steven David Pillay",
        "githubUrl": "https://github.com/code-Gambler/movie-recommender-api",
        "hostname": urlparse(request.base_url).hostname
    }

@app.route("/recommend", methods=["GET"])
def recommend():
    title = request.args.get('title')
    genre = request.args.get('genre')
    if title is not None:
        return get_recommendations(title)
    elif genre is not None:
        genre_list = list(genre.split(","))
        return get_recommendations_by_genre(genre_list)
    else:
        return json({"message":"No Title or Genre Specified!"})

if __name__ == '__main__':
    app.run(debug=True)