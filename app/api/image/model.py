from app import db, ma
from flask import current_app

class ImageModel(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    def get_uri(self):
        return current_app.config["IMAGES_URL"]+self.filename



class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        pass

