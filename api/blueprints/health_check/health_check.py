from urllib.parse import urlparse
from flask import Blueprint, request

health_check_bp = Blueprint("health_check", __name__)

@health_check_bp.route("/")
def health_check():
    return {
        "author": "Steven David Pillay",
        "githubUrl": "https://github.com/code-Gambler/movie-recommender-api",
        "hostname": urlparse(request.base_url).hostname
    }