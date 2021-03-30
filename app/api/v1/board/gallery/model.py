from app import db, ma
from marshmallow.validate import Length


class GalleryModel(db.Model):
    __tablename__ = "gallery"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.String(255), nullable=True)
    manager_user_id = db.Column(
        db.String(320), db.ForeignKey("user.email"), nullable=False
    )

    posts = db.relationship("PostModel", passive_deletes=True, backref="posted_gallery")

    def delete_gallery(self):
        db.session.delete(self)

    def is_manager(self, user):
        return user.email == self.manager_user_id

    def patch(self, name, explain):
        self.name = name if name is not None else self.name
        self.explain = explain if explain is not None else self.explain

        db.session.commit()


class GallerySchema(ma.SQLAlchemySchema):
    class Meta:
        model = GalleryModel

    name = ma.auto_field()
    explain = ma.auto_field()
    id = ma.auto_field()


gallery_schema = GallerySchema()
galleries_schema = GallerySchema(many=True, only=("name", "id"))


class GalleryPostValidateSchema(ma.Schema):
    name = ma.Str(requierd=True, validate=Length(max=30, min=1))
    explain = ma.Str(requierd=True, validate=Length(max=255, min=0))


class GalleryPatchValidateSchema(ma.Schema):
    name = ma.Str(requierd=False, validate=Length(max=255, min=0))
    explain = ma.Str(requierd=False)
