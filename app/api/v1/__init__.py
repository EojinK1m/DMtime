from flask.blueprints import Blueprint

from app.api.v1.image import image_api
from app.api.v1.board import board_api
from app.api.v1.user import user_api, account_api
from app.api.v1.auth import auth_api
from app.api.v1.general import view


v1_blueprint = Blueprint('api_v1', 'api_v1')

v1_blueprint.after_request(view.commit_session_after_request)
v1_blueprint.teardown_request(view.rollback_session_when_error)

board_api.init_app(v1_blueprint)
user_api.init_app(v1_blueprint)
account_api.init_app(v1_blueprint)
image_api.init_app(v1_blueprint)
auth_api.init_app(v1_blueprint)