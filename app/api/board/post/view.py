from flask import make_response, request
from flask_restful import Resource

from app.api.board.post.service import PostService, PostListService



class PostList(Resource):
    def get(self):
     return make_response(PostListService.provide_post_list())

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

class PostLike(Resource):
    def get(self, post_id):
        return make_response(PostService.post_like(post_id))