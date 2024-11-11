from flask import Blueprint
from flask_cors import CORS

bp = Blueprint('products', __name__)
CORS(bp)

from . import routes