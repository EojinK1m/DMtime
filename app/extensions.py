from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis

from app.util.email_sender import EmailSender
from app.util.file_saver import FileSaver


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
redis_client = FlaskRedis()
email_sender = EmailSender()
file_saver = FileSaver()
