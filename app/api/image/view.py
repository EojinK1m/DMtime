from flask import request, make_response
from flask_restful import Resource

from app.api.image.service import ImageService


class ImageUpload(Resource):
    def post(self):
        return make_response(ImageService.image_upload(request.files['image']))

