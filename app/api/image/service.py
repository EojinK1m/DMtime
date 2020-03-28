import os
from flask import jsonify, current_app as app

from app import db
from app.api.image.model import ImageModel, ImageSchema




def is_correct_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_id_from_filename(filename):
    return int(filename.rsplit('.', 1)[0].lower())

def get_path_from_filename(filename):
    return os.path.join(app.config['IMAGE_UPLOADS'], filename)


class ImageService:


    @staticmethod
    def image_upload(image):
        if not image:
            return jsonify({'msg':'No image'}), 400

        filename = image.filename
        if filename == '':
            return jsonify({'msg':'No selected file'}), 400

        if not is_correct_image(filename):
            return jsonify({'msg':'This image has tension that not supported'}), 400

        image_column = ImageModel(filename='')
        db.session.add(image_column)
        db.session.commit()

        saved_file_name = str(image_column.id) + '.' +filename.rsplit('.', 1)[1].lower()
        image.save(os.path.join(app.config['IMAGE_UPLOADS'], saved_file_name))
        image_column.filename = saved_file_name
        db.session.commit()


        return jsonify({'msg':'Upload succeed',\
                        'image_info':ImageSchema(exclude=['filename']).dump(image_column)}), 200

    @staticmethod
    def get_filename_by_id(id):
        find_image_column = ImageModel.query.filter_by(id=id).first
        if not find_image_column:
            return None
        else:
            return find_image_column.filename




    @staticmethod
    def delete_image(id):
        delete_image_column = ImageModel.query.filter_by(id=id).first()

        if not delete_image_column:
            return False

        file_name = delete_image_column.filename

        os.remove(get_path_from_filename(file_name))
        db.session.delete(delete_image_column)

        db.session.commit()
        return True


    @staticmethod
    def set_foreign_key(image_id, key, location):
        image = ImageModel.query.filter_by(id=image_id).first()
        if not image:
            return False

        if location == 'user':
            image.user_id = key
        elif location == 'gallery':
            image.gallery_id = key
        elif location == 'post':
            image.post_id = key
        else:
            return False
        return True

