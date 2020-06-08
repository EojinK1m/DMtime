from app import db, ma
from marshmallow.validate import Length

class GalleryModel(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.String(255), nullable=True)

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


class GalleryPostValidateSchema(ma.Schema):
    name = ma.Str(requierd = True, validate = Length(max = 30, min = 1))
    explain = ma.Str(requierd = True, validate = Length(max = 255, min = 0))

class GalleryPatchValidateSchema(ma.Schema):
    name = ma.Str(requierd = False, validate = Length(max = 255, min = 0))
    explain = ma.Str(requierd = False)