from flask import Blueprint

mock_api = Blueprint('mock_api', __name__)

from . import mock
