from flask import Blueprint

power = Blueprint('power', __name__)

from . import power
