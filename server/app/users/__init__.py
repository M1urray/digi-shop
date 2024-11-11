from flask import Blueprint
from flask_cors import CORS

bp = Blueprint('users', __name__)
CORS(bp)

from . import routes