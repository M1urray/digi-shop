from flask import Blueprint
from flask_cors import CORS

bp = Blueprint('orders', __name__)
CORS(bp)

from . import routes