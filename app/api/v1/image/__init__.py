from flask_restful import Api

from app.api.v1.image.view import ImageUpload, Image

image_api = Api()
image_api.add_resource(ImageUpload, '/images')
image_api.add_resource(Image, '/images/<id>')


