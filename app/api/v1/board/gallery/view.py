from flask import make_response, request, abort
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.util.request_validator import RequestValidator
from app.api.v1.board.gallery.service import GalleryService, GalleryListService
from app.api.v1.board.gallery.model import galleries_schema, GalleryPostValidateSchema, gallery_schema

from app.api.v1.user.service import AccountService

class GalleryList(Resource):
    def get(self):
        galleries = GalleryListService.get_galleries()
        response_body = galleries_schema.dump(galleries)

        return response_body, 200

    @jwt_required
    def post(self):
        post_account = AccountService.find_user_by_email(get_jwt_identity())
        RequestValidator.validate_request(GalleryPostValidateSchema(), request.json)

        GalleryListService.create_new_gallery(
            name=request.json['name'],
            explain=request.json['explain'],
            manager_user=post_account
        )

        return {}, 201


class Gallery(Resource):
    def get(self, gallery_id):
        gallery = GalleryService.get_gallery_by_id(gallery_id)

        return gallery_schema.dump(gallery), 200

    @GalleryService.gallery_manager_required
    def patch(self, gallery_id):
        RequestValidator.validate_request(GalleryPostValidateSchema(), request.json)

        GalleryService.modify_gallery_info(
            gallery=GalleryService.get_gallery_by_id(gallery_id),
            name=request.json.get('name'),
            explain=request.json.get('explain')
        )

        return {}, 200

    @GalleryService.gallery_manager_required
    def delete(self, gallery_id):
        gallery2delete = GalleryService.get_gallery_by_id(gallery_id)

        GalleryService.delete_gallery(gallery2delete)

        return {}, 200