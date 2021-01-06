import os
from flask import jsonify, current_app as app, abort

from app import db
from app.api.v1.image.model import ImageModel, ImageSchema



def is_correct_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_id_from_filename(filename):
    return int(filename.rsplit('.', 1)[0].lower())

def get_path_from_filename(filename):
    return os.path.join(app.config['IMAGE_UPLOADS'], filename)


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

    @staticmethod
    def get_filename_by_id(id):
        find_image_column = ImageModel.query.filter_by(id=id).first
        if not find_image_column:
            return None
        else:
            return find_image_column.filename

    @classmethod
    def delete_image(cls, id):
        delete_image_column = cls.__get_image_by_id(id)

        file_name = delete_image_column.filename

        os.remove(get_path_from_filename(file_name))
        db.session.delete(delete_image_column)

        return True

    @classmethod
    def set_foreign_key(cls, image_id, key, location):
        image = cls.__get_image_by_id(image_id)

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