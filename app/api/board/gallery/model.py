from app import db, ma

class GalleryModel(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.Text, nullable=True)

    posts = db.relationship('PostModel', backref='gallery')

    def delete_gallery(self):
        db.session.delete(self)



class GallerySchema(ma.SQLAlchemySchema):
    class Meta:
        model = GalleryModel

    name = ma.auto_field()
    explain = ma.auto_field()
    id = ma.auto_field()


gallery_schema  = GallerySchema()
galleries_schema = GallerySchema(many=True, only=('name', 'id'))