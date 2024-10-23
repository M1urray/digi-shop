from flask import Blueprint

bp = Blueprint('hotdeals', __name__)

from . import routes