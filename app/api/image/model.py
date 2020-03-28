from app import db, ma
from flask import current_app

class ImageModel(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)


class ImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ImageModel()


    url = ma.Method(serialize='get_uri', deserialize='get_uri')
    filename = ma.auto_field()
    id = ma.auto_field()

    def get_uri(self, obj):
        return current_app.config["IMAGES_URL"]+obj.filename





