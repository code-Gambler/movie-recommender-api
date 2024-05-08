from urllib.parse import urlparse
from flask import Blueprint, request

health_check_bp = Blueprint("health_check", __name__)

@health_check_bp.route("/")
def health_check():
    """Performs a basic health check for the API.

    This function defines a route handler for the root path (`/`) of the `health_check` Blueprint.
    It returns a JSON dictionary containing basic information about the API, including:
     - Author: Name of the API author.
     - githubUrl: URL of the API's GitHub repository.
     - hostname: The hostname of the server running the API (extracted from the request).

    Returns:
        A JSON dictionary containing the health check information.
    """
    return {
        "author": "Steven David Pillay",
        "githubUrl": "https://github.com/code-Gambler/movie-recommender-api",
        "hostname": urlparse(request.base_url).hostname
    }