from flask import Blueprint

bp = Blueprint('specification', __name__)

from . import routes