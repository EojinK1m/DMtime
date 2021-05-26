from flask import Flask
from .extensions import (
    file_saver,
    ma,
    db,
    jwt,
    redis_client,
    email_sender,
    bcrypt
)
from redis import ConnectionError

from app.util.email_sender import EmailSender
from app.util.file_saver import FileSaver

import time
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    import_models()

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)
    email_sender.init_app(app)
    file_saver.init_app(app)

    wait_db_ready(app)
    wait_redis_ready(app)


    with app.app_context():
        db.create_all()

    from app.api.v1 import v1_blueprint
    app.register_blueprint(v1_blueprint, url_prefix="/api/v1")

    return app


def wait_db_ready(app):
    wait_db_ready.num_of_try = 0

    while True:
        try:
            with app.app_context():
                db.session.query("1").from_statement(text("SELECT 1")).all()
            return True
        except OperationalError:
            time.sleep(0.5)
            if wait_db_ready.num_of_try >= 20:
                raise Exception("db not work!")
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
            time.sleep(0.5)
            if wait_db_ready.num_of_try >= 20:
                raise Exception("redis not work!")
            else:
                wait_db_ready.num_of_try += 1
            continue
        except Exception as e:
            raise e


def import_models():
    import app.api.v1.user.model

    import app.api.v1.gallery.model
    import app.api.v1.image.model
    import app.api.v1.post.model
    import app.api.v1.report.model
    import app.api.v1.comment.model
    import app.api.v1.postlike.model