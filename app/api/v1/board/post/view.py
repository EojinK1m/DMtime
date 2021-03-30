from datetime import datetime

from flask import make_response, request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.util.request_validator import RequestValidator

from app import db
from app.api.v1.board.post.service import (
    PostService,
    PostListService,
    PostLikeService,
)
from app.api.v1.board.post.model import (
    posts_schema,
    post_schema,
    posts_schema_user,
    PostGetQueryParameterValidateSchema,
    PostPostInputValidateSchema,
    PostResourceQueryParameterValidateSchema,
    PostPatchInputValidateSchema,
)
from app.api.v1.board.gallery.service import GalleryService
from app.api.v1.user.service import AccountService
from app.api.v1.user.service import UserService
from app.api.v1.image.service import ImageService


class PostList(Resource):
    def get(self):
        RequestValidator.validate_request(
            PostGetQueryParameterValidateSchema(), request.args
        )

        gallery_id = request.args.get(key="gallery-id", default=None, type=int)
        username = request.args.get(key="username", default=None, type=str)
        page = request.args.get(key="page", default=1, type=int)
        per_page = request.args.get(key="per-page", default=20, type=int)

        if gallery_id and username:
            abort(400)
        elif gallery_id is None and username is None:
            posts = PostListService.get_posts_with_paging(
                per_page=per_page, page=page
            )
        elif gallery_id is not None:
            posts = PostListService.get_posts_by_gallery_with_paging(
                gallery=GalleryService.get_gallery_by_id(gallery_id),
                per_page=per_page,
                page=page,
            )
        elif username is not None:
            posts = PostListService.get_posts_by_user_with_paging(
                user=UserService.get_user_by_username(username),
                per_page=per_page,
                page=page,
            )

        return {
            "posts": posts_schema.dump(posts.items),
            "number_of_pages": posts.pages,
        }, 200

    @jwt_required
    def post(self):
        json = request.get_json()
        args = request.args

        RequestValidator.validate_request(
            PostResourceQueryParameterValidateSchema(), args
        )
        RequestValidator.validate_request(PostPostInputValidateSchema(), json)

        post_gallery = GalleryService.get_gallery_by_id(
            args.get(key="gallery-id", type=int)
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

        for image_id in json["image_ids"]:
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


class PostLike(Resource):
    @jwt_required
    def post(self, post_id):
        post = PostService.get_post_by_post_id(post_id)
        request_account = AccountService.find_user_by_email(get_jwt_identity())

        postlike = PostLikeService.get_postlike_by_post_and_account(
            post=post, account=request_account
        )

        if postlike:
            PostLikeService.delete_postlike(postlike)
            message = "Cancel post like"
        else:
            PostLikeService.create_postlike(account=request_account, post=post)
            message = "Like post"

        db.session.commit()
        return {"message": message, "likes": len(post.postlikes)}, 200
