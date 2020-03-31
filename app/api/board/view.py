from flask import make_response, request
from flask_restful import Resource

from app.api.board.service import PostService, PostListService,\
                                GalleryService, GalleryListService

class PostList(Resource):
    def get(self):
        gallery_id = request.args.get('gallery-id', None)
        return make_response(PostListService.provide_post_list(gallery_id))

    def post(self):
        gallery_id = request.args.get('gallery-id', None)
        return make_response(PostListService.post_post(gallery_id, request.json))

class Post(Resource):
    def get(self, post_id):
        return make_response(PostService.provide_post(post_id))
    def patch(self, post_id):
        return make_response(PostService.modify_post(post_id))
    def delete(self, post_id):
        return make_response(PostService.delete_post(post_id))

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