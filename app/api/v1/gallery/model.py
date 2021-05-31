from app.extensions import db, ma
from marshmallow.validate import Length, Range

GALLERY_TYPES = {"special": 0, "default": 1, "user": 2}


class GalleryModel(db.Model):
    __tablename__ = "gallery"

    gallery_id = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.String(255), nullable=True)
    manager_user_id = db.Column(
        db.String(320),
        db.ForeignKey(
            "user.email",
            ondelete="CASCADE"
        )
    )
    gallery_type = db.Column(db.Integer(), nullable=False)

    posts = db.relationship(
        "PostModel", passive_deletes=True, backref="posted_gallery"
    )

    def delete_gallery(self):
        db.session.delete(self)

    def is_manager(self, user):
        return user.email == self.manager_user_id

    def patch(self, name, explain):
        self.name = name if name is not None else self.name
        self.explain = explain if explain is not None else self.explain

        db.session.commit()

    @property
    def id(self):
        return self.gallery_id

class GallerySchema(ma.SQLAlchemySchema):
    class Meta:
        model = GalleryModel

    name = ma.auto_field()
    explain = ma.auto_field()
    gallery_id = ma.auto_field()
    gallery_type = ma.auto_field()


gallery_schema = GallerySchema()
galleries_schema = GallerySchema(many=True)


class GetGalleriesQueryParameterValidateSchema(ma.Schema):
    gallery_type = ma.Integer(
        requierd=False,
        allow_none=False,
        validate=Range(min=0, max=2),
        data_key="gallery-type",
    )


class PostGalleryValidateSchema(ma.Schema):
    name = ma.Str(required=True, validate=Length(max=30, min=1), allow_none=False)
    explain = ma.Str(required=True, validate=Length(max=255, min=0))
    gallery_id = ma.Str(required=True, validate=Length(max=30, min=1))
    gallery_type = ma.Integer(
        required=True,
        allow_none=False,
        validate=Range(min=0, max=2),
    )


class PatchGalleryValidateSchema(ma.Schema):
    name = ma.Str(required=False, validate=Length(max=255, min=0))
    explain = ma.Str(required=False)
