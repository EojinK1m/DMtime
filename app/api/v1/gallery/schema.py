from marshmallow.validate import Range, Length

from app import ma
from app.api.v1.gallery.model import GalleryModel
from app.api.v1.general.service import get_user_from_token


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