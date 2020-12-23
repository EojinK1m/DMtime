from app import db, ma
from flask import current_app
from marshmallow import ValidationError

class ImageModel(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
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
    def validate_is_image_allowed_extension(image):
        try:
            extension = image.filename.rsplit('.', 1)[-1].lower()
        except IndexError:
            raise ValidationError('Server can not parse extension from filename.')

        if not extension in current_app.config['ALLOWED_EXTENSIONS']:
            raise ValidationError(f'.{extension} is not allowed extension.')


    image = ma.Raw(required=True, validate=validate_is_image_allowed_extension)