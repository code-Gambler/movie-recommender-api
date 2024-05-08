import sys
import json
from flask import Blueprint, request
from pathlib import Path
# #Adding our recommend
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent) + "/recommend-logic")

from recommend import get_recommendations, get_recommendations_by_genre

v1_bp = Blueprint("v1", __name__, url_prefix="/v1")

@v1_bp.route("/recommend")
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