from flask import make_response, request, abort
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.api.v1.board.gallery.service import GalleryService, GalleryListService
from app.api.v1.board.gallery.model import galleries_schema, GalleryPostValidateSchema

from app.api.v1.user.account.service import AccountService

class GalleryList(Resource):
    def get(self):
        galleries = GalleryListService.get_galleries()
        response_body = galleries_schema.dump(galleries)

        return response_body, 200

    @jwt_required
    def post(self):
        post_account = AccountService.find_account_by_email(get_jwt_identity())
        error = GalleryPostValidateSchema().validate(request.json)
        if error:
            abort(400)

        gallery_data2post = request.json

        GalleryListService.create_new_gallery(
            name=gallery_data2post['name'],
            explain=gallery_data2post['explain'],
            manager_user=post_account.user
        )

        return 200


class Gallery(Resource):
    def get(self, gallery_id):
        return make_response(GalleryService.provide_gallery_info(gallery_id=gallery_id))

    def patch(self, gallery_id):
        return make_response(GalleryService.modify_gallery_info(gallery_id=gallery_id))

    def delete(self, gallery_id):
        return make_response(GalleryService.delete_gallery(gallery_id=gallery_id))