from flask import Blueprint
from flask_restful import Api

from app.api.image.view import ImageUpload

image_blueprint = Blueprint('image api', 'image api')
image_api = Api(image_blueprint)
image_api.add_resource(ImageUpload, '/')

