from flask import Flask, jsonify, request
from urllib.parse import urlparse
app = Flask(__name__)

@app.route('/')
def health_check():
    return {
        "author": "Steven David Pillay",
        "githubUrl": "https://github.com/code-Gambler/movie-recommender-api",
        "version": "0.0.1",
        "hostname": urlparse(request.base_url).hostname
    }



if __name__ == '__main__':
    app.run(debug=True)