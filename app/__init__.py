from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from redis import ConnectionError

from app import config
from app.util.email_sender import EmailSender

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
redis_client = FlaskRedis()
email_sender = EmailSender()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)
    email_sender.init_app(app)

    wait_db_ready(app)
    wait_redis_ready(app)

    with app.app_context():
        db.create_all()


    from app.api.v1.image import image_blueprint
    from app.api.v1.board import board_blueprint
    from app.api.v1.user import user_blueprint
    from app.api.v1.user import account

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
            if wait_db_ready.num_of_try >= 20:
                raise Exception('db not work!')
            else:
                wait_db_ready.num_of_try += 1
            continue
        except Exception as e:
            raise e


def wait_redis_ready(app):
    wait_db_ready.num_of_try = 0

    while True:
        try:
            with app.app_context():
                redis_client.ping()
            return True
        except ConnectionError:
            time.sleep(.5)
            if wait_db_ready.num_of_try >= 20:
                raise Exception('redis not work!')
            else:
                wait_db_ready.num_of_try += 1
            continue
        except Exception as e:
            raise e


