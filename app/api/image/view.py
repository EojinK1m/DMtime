from flask import request, make_response, jsonify
from flask_restful import Resource

from app.api.image.service import ImageService


class ImageUpload(Resource):
    def post(self):
        return make_response(ImageService.image_upload(request.files['image']))

class Image(Resource):
    def delete(self, id):
        if not ImageService.delete_image(id):
            return make_response(jsonify(msg='image not found'), 404)
        else:
            return make_response(jsonify(msg='image deleted'), 200)

