from flask import Blueprint

bp = Blueprint('brands', __name__)


from . import routes