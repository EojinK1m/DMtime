from flask.blueprints import Blueprint

from app.api.v1.image import image_api
from app.api.v1.board import board_api
from app.api.v1.user import user_api, account_api

v1_blueprint = Blueprint('api_v1', 'api_v1')

board_api.init_app(v1_blueprint)
user_api.init_app(v1_blueprint)
account_api.init_app(v1_blueprint)
image_api.init_app(v1_blueprint)