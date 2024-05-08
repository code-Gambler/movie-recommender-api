import os
from dotenv import load_dotenv
from flask import Flask
from blueprints.health_check.health_check import health_check_bp
from blueprints.api.api import api_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(health_check_bp)
    app.register_blueprint(api_bp)
    return app

if __name__ == '__main__':
    current_port = 5000
    if os.getenv("PORT"):
        current_port = os.getenv("PORT")
    create_app().run(host='0.0.0.0', port=current_port, debug=True)