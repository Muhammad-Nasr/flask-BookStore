from flask import Blueprint

bp = Blueprint('error', __name__)

from main.errors import handlers
