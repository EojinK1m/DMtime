from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.util.request_validator import RequestValidator
from app.api.v1.gallery.service import GalleryService, GalleryListService
from app.api.v1.gallery.model import (
    GALLERY_TYPES
)
from app.api.v1.gallery.schema import gallery_schema, galleries_schema, GetGalleriesQueryParameterValidateSchema, \
    PostGalleryValidateSchema, PatchGalleryValidateSchema
from app.api.v1.general.service import verify_admin_jwt_in_request
from app.api.v1.user.service import AccountService


class GalleryList(Resource):
    def get(self):
        RequestValidator.validate_request(
            schema=GetGalleriesQueryParameterValidateSchema(),
            data=request.args,
        )

        galleries = GalleryListService.get_galleries(
            gallery_type=request.args.get("gallery-type", type=int)
        )
        return galleries_schema.dump(galleries), 200

    @jwt_required
    def post(self):
        post_account = AccountService.find_user_by_email(get_jwt_identity())

        RequestValidator.validate_request(
            PostGalleryValidateSchema(), request.json
        )
        gallery_type = request.json["gallery_type"]

        if self.is_gallery_type_for_admin(gallery_type):
            verify_admin_jwt_in_request()

        GalleryListService.create_new_gallery(
            gallery_id=request.json["gallery_id"],
            name=request.json["name"],
            explain=request.json["explain"],
            gallery_type=gallery_type,
            manager_user=post_account,
        )

        return {}, 201

    def is_gallery_type_for_admin(self, gallery_type):
        return gallery_type != GALLERY_TYPES["user"]


class Gallery(Resource):
    def get(self, gallery_id):
        gallery = GalleryService.get_gallery_by_id(gallery_id)

        return gallery_schema.dump(gallery), 200

    @GalleryService.gallery_manager_required
    def patch(self, gallery_id):
        RequestValidator.validate_request(
            PatchGalleryValidateSchema(), request.json
        )

        GalleryService.modify_gallery_info(
            gallery=GalleryService.get_gallery_by_id(gallery_id),
            name=request.json.get("name"),
            explain=request.json.get("explain"),
        )

        return {}, 200

    @GalleryService.gallery_manager_required
    def delete(self, gallery_id):
        gallery2delete = GalleryService.get_gallery_by_id(gallery_id)

        GalleryService.delete_gallery(gallery2delete)

        return {}, 200
