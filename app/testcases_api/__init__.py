from flask import Blueprint

testcases_api = Blueprint('testcases_api', __name__)

from . import testcase
