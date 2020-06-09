from flask import make_response, request
from flask_restful import Resource

from app.api.board.gallery.service import GalleryService, GalleryListService



class GalleryList(Resource):
    def get(self):
        return make_response(GalleryListService.provide_gallery_list())
    def post(self):
        return make_response(GalleryListService.create_gallery(request.json))

class Gallery(Resource):
    def get(self, gallery_id):
        return make_response(GalleryService.provide_gallery_info(gallery_id))

    def patch(self, gallery_id):
        return make_response(GalleryService.modify_gallery_info(gallery_id))

    def delete(self, gallery_id):
        return make_response(GalleryService.delete_gallery(gallery_id))