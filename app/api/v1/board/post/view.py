from datetime import datetime

from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.util.request_validator import RequestValidator

from app import db
from app.api.v1.board.post.service import (
    PostService,
    PostListService
)
from app.api.v1.board.post.model import (
    posts_schema,
    post_schema,
    PostGetQueryParameterValidateSchema,
    PostPostInputValidateSchema,
    PostResourceQueryParameterValidateSchema,
    PostPatchInputValidateSchema,
)
from app.api.v1.board.gallery.service import GalleryService
from app.api.v1.user.service import AccountService
from app.api.v1.user.service import UserService
from app.api.v1.image.service import ImageService
from ...auth.service import TokenService


class PostList(Resource):
    def get(self):
        RequestValidator.validate_request(
            PostGetQueryParameterValidateSchema(), request.args
        )

        gallery_id = request.args.get(key="gallery-id", default=None, type=str)
        username = request.args.get(key="username", default=None, type=str)
        page = request.args.get(key="page", default=1, type=int)
        per_page = request.args.get(key="per-page", default=20, type=int)

        gallery = GalleryService.get_gallery_by_id(gallery_id) if gallery_id else None
        user = UserService.get_user_by_username(username) if username else None

        paged_posts = PostListService.get_paginated_posts(
            gallery=gallery,
            user=user,
            page=page,
            per_page=per_page
        )

        return {
            "posts": posts_schema.dump(paged_posts.items),
            "number_of_pages": paged_posts.pages,
        }, 200

    @jwt_required
    def post(self):
        json = request.json
        args = request.args

        RequestValidator.validate_request(
            PostResourceQueryParameterValidateSchema(), args
        )
        RequestValidator.validate_request(PostPostInputValidateSchema(), json)

        post_gallery = GalleryService.get_gallery_by_id(
            args.get(key="gallery-id")
        )
        uploader_account = AccountService.find_user_by_email(
            get_jwt_identity()
        )

        created_post = PostListService.create_post(
            content=json["content"],
            title=json["title"],
            is_anonymous=json["is_anonymous"],
            upload_user=uploader_account,
            post_gallery=post_gallery,
            posted_datetime=datetime.now(),
        )

        for image_id in json["images"]:
            ImageService.set_foreign_key(
                image_id=image_id, key=created_post.id, location="post"
            )

        return {}, 201


class HotPostList(Resource):
    def get(self):
        RequestValidator.validate_request(
            PostGetQueryParameterValidateSchema(), request.args
        )
        page = request.args.get(key="page", default=1, type=int)
        per_page = request.args.get(key="per_page", default=20, type=int)

        posts = PostListService.get_posts_for_days(7)
        PostListService.sort_posts_by_hot_score(posts)
        posts, number_of_pages = PostListService.paging_posts(
            posts=posts, page=page, per_page=per_page
        )

        return {
            "posts": posts_schema.dump(posts),
            "number_of_page": number_of_pages,
        }, 200


class Post(Resource):
    @jwt_required
    def get(self, post_id):
        post = PostService.get_post_by_post_id(post_id)

        post.increase_view()

        return post_schema.dump(post), 200

    @jwt_required
    def patch(self, post_id):
        request_account = AccountService.find_user_by_email(get_jwt_identity())
        post = PostService.get_post_by_post_id(post_id)
        json = request.json

        PostService.check_post_access_permission_of_account(
            post=post, account=request_account
        )
        RequestValidator.validate_request(PostPatchInputValidateSchema(), json)

        PostService.update_post(
            post=post,
            content=json.get("content", post.content),
            title=json.get("title", post.title),
        )

        new_images_ids, delete_images_ids = PostService.get_diff_of_images(
            post, json.get("image_ids", [])
        )

        for image_id_to_delete in delete_images_ids:
            ImageService.delete_image_by_id(image_id_to_delete)
        for image_id_to_register in new_images_ids:
            ImageService.set_foreign_key(image_id_to_register, post.id, "post")

        db.session.commit()
        return {}, 200

    @jwt_required
    def delete(self, post_id):
        request_account = AccountService.find_user_by_email(get_jwt_identity())
        post = PostService.get_post_by_post_id(post_id)

        PostService.check_post_access_permission_of_account(
            post=post, account=request_account, admin_allow=True
        )

        PostService.delete_post(post)

        db.session.commit()
        return {}, 200


class UserLikedPostList(Resource):
    def get(self, username):

        user_liked_posts = PostListService.get_user_liked_posts(
            UserService.get_user_by_username(username)
        )

        return posts_schema.dump(user_liked_posts)


class RequestUserLikedPostList(Resource):
    @jwt_required
    def get(self):
        user_liked_posts = PostListService.get_user_liked_posts(
            TokenService.get_user_from_token()
        )

        return posts_schema.dump(user_liked_posts)
