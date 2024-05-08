import sys
import json
from flask import Blueprint, request
from pathlib import Path

# Adding our recommend module path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent) + "/recommend-logic")
from recommend import get_recommendations, get_recommendations_by_genre

v1_bp = Blueprint("v1", __name__, url_prefix="/v1")

@v1_bp.route("/recommend")
def recommend():
    """Recommends movies based on title or genre.

    This function defines a route handler for the `/recommend` endpoint within the `v1` Blueprint.
    It accepts two optional query parameters:

    - title (str): The title of a movie to use for recommendations based on similar user ratings and content.
    - genre (str, comma-separated): A comma-separated list of genres to filter recommendations by (case-insensitive).

    If both `title` and `genre` are missing, it returns an error message.
    Otherwise, it calls the appropriate functions from the `recommend` module:

     - If `title` is provided, it calls `get_recommendations(title)` to get recommendations based on the title.
     - If `genre` is provided, it splits the comma-separated string into a list and calls
       `get_recommendations_by_genre(genre_list)` to get recommendations based on the genre(s).

    The function returns a JSON response containing an error message.

    Returns:
        A JSON response containing the recommended movies or an error message.
    """
    title = request.args.get('title')
    genre = request.args.get('genre')
    if title is not None:
        return get_recommendations(title)
    elif genre is not None:
        genre_list = list(genre.split(","))
        return get_recommendations_by_genre(genre_list)
    else:
        return json({"message":"No Title or Genre Specified!"})