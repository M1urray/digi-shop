from flask import Blueprint
from flask_cors import CORS

bp = Blueprint('specification', __name__)
CORS(bp)
from . import routes