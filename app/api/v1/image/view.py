import os
import imghdr

from flask import request, current_app
from flask_restful import Resource

from app import db
from app.util.random_string_generator import generate_random_string

from app.util.request_validator import RequestValidator
from app.api.v1.image.service import ImageService
from app.api.v1.image.model import PostImageValidateSchema


class ImageUpload(Resource):
    def post(self):
        def validate_image_file(image):
            RequestValidator.validate_request(
                PostImageValidateSchema(), {"image": image}
            )
            return image

        def get_extension_from_image(file):
            return imghdr.what(file.stream)

        def save_image_file_2_storage(image):
            image.save(
                os.path.join(
                    current_app.config["IMAGE_UPLOADS"], image.filename
                )
            )

        image_file = validate_image_file(request.files.get("image"))
        file_name_for_save = self.generate_filename(get_extension_from_image(image_file))

        ImageService.create_image(file_name=file_name_for_save)
        image_file.filename = file_name_for_save
        save_image_file_2_storage(image_file)

        return {}, 201

    @staticmethod
    def generate_filename(extension):
        while True:
            filename = generate_random_string(10) + '.' + extension

            if ImageService.get_image_by_id_or_none(filename) is None:
                return filename


class Image(Resource):
    def delete(self, id):
        ImageService.delete_image(ImageService.get_image_by_id(id))

        db.session.commit()
        return {}, 200
