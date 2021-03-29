import os
from flask import current_app as app, abort

from app import db
from app.api.v1.image.model import ImageModel


class ImageService:

    @classmethod
    def create_image(cls, file_name='', user_id=None, post_id=None, gallery_id=None):
        image = ImageModel(
            filename = file_name,
            user_id = user_id,
            post_id = post_id,
            gallery_id = gallery_id
        )

        db.session.add(image)
        db.session.flush()

        return image

    @classmethod
    def update_image(cls, image, file_name='', user_id=None, post_id=None, gallery_id=None):
        image.filename = file_name
        image.user_id = user_id
        image.post_id = post_id
        image.gallery_id = gallery_id

        db.session.flush()

    @classmethod
    def get_image_by_id(cls, image_id):
        image = ImageModel.query.filter_by(id=image_id).first()

        if image is None:
            abort(404, f'Image{image_id} s not found.')

        return image

    @classmethod
    def delete_image(cls, image):
        def delete_file_from_storage(file_2_delete):
            os.remove(get_path_from_filename(file_2_delete.filename))

        def get_path_from_filename(filename):
            return os.path.join(app.config['IMAGE_UPLOADS'], filename)

        try:
            delete_file_from_storage(image)
            db.session.delete(image)
            db.session.flush()
        except Exception:
            db.session.rollback()
            abort(500, 'An error occur while deleting image.')

    @classmethod
    def delete_image_by_id(cls, id):
        image = cls.get_image_by_id(id)
        cls.delete_image(image)

    @classmethod
    def set_foreign_key(cls, image_id, key, location):
        image = cls.get_image_by_id(image_id)

        if image.post_id or image.user_id or image.gallery_id:
            abort(409, 'Image is included in other content.')

        try:
            if location == 'user':
                image.user_id = key
            elif location == 'gallery':
                image.gallery_id = key
            elif location == 'post':
                image.post_id = key
            else:
                raise ValueError()
        except:
            abort(500, 'Exception while set image')

        db.session.flush()