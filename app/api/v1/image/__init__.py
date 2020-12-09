from app.api.v1 import v1_blueprint
from flask_restful import Api

from app.api.v1.image.view import ImageUpload, Image

image_api = Api(v1_blueprint)
image_api.add_resource(ImageUpload, '/images')
image_api.add_resource(Image, '/images/<id>')


