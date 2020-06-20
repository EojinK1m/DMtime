from flask import Flask
from app import config

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager



db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()




def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)


    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.api.image.model import ImageModel
    from app.api.board.post.model import PostModel
    from app.api.board.gallery.model import GalleryModel
    from app.api.user.model import UserModel
    from app.api.user.account.model import AccountModel

    wait_db_ready(app)

    with app.app_context():
        db.create_all()


    from app.api.image import image_blueprint
    from app.api.board import board_blueprint
    from app.api.user import user_blueprint
    from app.api.user import account

    app.register_blueprint(board_blueprint, url_prefix='/api/board')
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.register_blueprint(image_blueprint, url_prefix='/api/images')

    return app


from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['roles'] == 'admin':
            return jsonify(msg='Access denied, admin only!'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


import time
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

def wait_db_ready(app):
    wait_db_ready.num_of_try = 0

    while True:
        try:
            with app.app_context():
                db.session.query("1").from_statement(text("SELECT 1")).all()
            return True
        except OperationalError:
            time.sleep(.5)
            if wait_db_ready.num_of_try >= 10:
                raise Exception('db not work!')
            else:
                wait_db_ready.num_of_try += 1
            continue
        except Exception as e:
            raise e


