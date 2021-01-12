import imghdr

from app import db, ma
from flask import current_app
from marshmallow import ValidationError

class ImageModel(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(320), db.ForeignKey('user.email', ondelete="CASCADE"), nullable=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id', ondelete='CASCADE'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=True)


class ImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ImageModel()

    url = ma.Method(serialize='get_uri', deserialize='get_uri')
    filename = ma.auto_field()
    id = ma.auto_field()

    def get_uri(self, obj):
        return current_app.config["IMAGES_URL"]+obj.filename


class PostImageValidateSchema(ma.Schema):

    @staticmethod
    def validate_image(image):
        type_of_image = imghdr.what(image.stream)

        error = ''
        if type_of_image is None:
            error = 'Requested file is not image file.'
        elif not type_of_image in current_app.config['ALLOWED_EXTENSIONS']:
            error = f'.{type_of_image} is not allowed extension.'

        if error:
            raise ValidationError(error)

    image = ma.Raw(
        required=True,
        validate=validate_image.__func__,
        error_messages={
            "null": "This request must include image file.",
        }
    )