from datetime import datetime

from flask import make_response, request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.util.request_validator import RequestValidator

from app.api.v1.board.post.service import PostService, PostListService
from app.api.v1.board.post.model import \
    posts_schema,\
    posts_schema_user,\
    PostGetQueryParameterValidateSchema, \
    PostPostInputValidateSchema, \
    PostResourceQueryParameterValidateSchema
from app.api.v1.board.gallery.service import GalleryService
from app.api.v1.user.account.service import AccountService
from app.api.v1.user.service import UserService
from app.api.v1.image.service import ImageService

class PostList(Resource):
    def get(self):
        RequestValidator.validate_request(PostGetQueryParameterValidateSchema(), request.args)

        gallery_id = request.args.get(key='gallery-id', default=None, type=int)
        username = request.args.get(key='username', default=None, type=str)
        page = request.args.get(key='page', default=1, type=int)
        per_page = request.args.get(key='per-page', default=20, type=int)

        if gallery_id and username:
            abort(400)

        if gallery_id is None and username is None:
          posts = PostListService.get_posts_with_paging(
              per_page=per_page,
              page=page
          )
          convert_schema = posts_schema
        elif gallery_id is not None:
            posts = PostListService.get_posts_by_gallery_with_paging(
                gallery=GalleryService.get_gallery_by_id(gallery_id),
                per_page=per_page,
                page=page
            )
            convert_schema = posts_schema
        elif username is not None:

            posts = PostListService.get_posts_by_user_with_paging(
                user=UserService.get_user_by_username(username),
                per_page=per_page,
                page=page
            )
            convert_schema = posts_schema_user

        return {
                   'posts': convert_schema.dump(posts.items),
                   'number_of_pages': posts.pages
               }, 200

    @jwt_required
    def post(self):
        json = request.get_json()
        args = request.args

        RequestValidator.validate_request(PostResourceQueryParameterValidateSchema(), args)
        RequestValidator.validate_request(PostPostInputValidateSchema(), json)

        post_gallery = GalleryService.get_gallery_by_id(args.get(key='gallery-id', type=int))
        uploader_account = AccountService.find_account_by_email(get_jwt_identity())

        created_post = PostListService.create_post(
            content=json['content'],
            title=json['title'],
            is_anonymous=json['is_anonymous'],
            upload_user=uploader_account.user,
            post_gallery=post_gallery,
            posted_datetime=datetime.now()
        )

        for image_id in json['image_ids']:
            ImageService.set_foreign_key(image_id=image_id, key=created_post.id, location='post')

        return {}, 200


class HotPostList(Resource):
    def get(self):
        return make_response(PostListService.provide_hot_post_list())


class Post(Resource):
    def get(self, post_id):
        return make_response(PostService.provide_post(post_id))

    def patch(self, post_id):
        return make_response(PostService.modify_post(post_id))

    def delete(self, post_id):
        return make_response(PostService.delete_post(post_id))


class PostLike(Resource):
    def post(self, post_id):
        return make_response(PostService.post_like(post_id))

