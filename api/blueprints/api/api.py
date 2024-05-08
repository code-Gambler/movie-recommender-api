from flask import Blueprint
from blueprints.api.v1.v1 import v1_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.register_blueprint(v1_bp)
