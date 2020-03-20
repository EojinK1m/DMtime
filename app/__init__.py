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

from app.api.board import board_blueprint
from app.api.user import user_blueprint
from app.api.user import account

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(board_blueprint, url_prefix='/api/board')
    app.register_blueprint(user_blueprint, url_prefix='/api/user')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app


