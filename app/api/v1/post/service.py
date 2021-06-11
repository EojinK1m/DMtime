import math
from datetime import datetime, timedelta

from flask import abort
from flask_jwt_extended import get_jwt_identity, get_jwt_claims

from app.extensions import db
from app.api.v1.post.model import PostModel

from ..comment.model import CommentModel
from app.api.v1.user.model import UserModel

from ..postlike.model import PostlikeModel


def check_user_permission(post):
    identify = get_jwt_identity()
    roles = get_jwt_claims()["roles"]
    if roles == "admin":
        return True
    user = UserModel.query.filter_by(email=identify).first().user
    return user.id == post.uploader.id


class PostService:

    @staticmethod
    def get_post_by_post_id(post_id):
        find_post = PostModel.query.filter_by(id=post_id).first()

        if find_post is None:
            abort(404, f"Post {post_id} is not found")

        return find_post

    @staticmethod
    def delete_post(post):
        post.delete_post()
        db.session.flush()

    @staticmethod
    def update_post(post, title, content):
        post.title = title
        post.content = content

        db.session.flush()

    @staticmethod
    def check_post_access_permission_of_account(
        post, account, admin_allow=False
    ):
        permission = account.email == post.uploader_id

        if admin_allow:
            if account.is_admin():
                permission = True

        if permission is False:
            abort(403, "Access denied.")

    @staticmethod
    def abort_if_not_exist_post_id(post_id):
        if PostModel.query.get(post_id) == None:
            abort(404, "post not found")

    @classmethod
    def get_diff_of_images(cls, post, image_ids):
        before_image_ids = [image.id for image in post.images]
        new_images_ids = [id for id in image_ids if not id in before_image_ids]
        delete_images_ids = [
            id for id in before_image_ids if not id in image_ids
        ]

        return new_images_ids, delete_images_ids


class PostListService:
    @staticmethod
    def create_post(
        content,
        title,
        upload_user,
        post_gallery,
        is_anonymous,
        posted_datetime,
    ):
        new_post = PostModel(
            content=content,
            title=title,
            uploader_id=upload_user.email,
            gallery_id=post_gallery.id,
            is_anonymous=is_anonymous,
            posted_datetime=posted_datetime,
        )

        db.session.add(new_post)
        db.session.flush()

        return new_post

    @staticmethod
    def get_posts_for_days(days):
        post_deadline = datetime.now() - timedelta(days=days)

        return PostModel.query.filter(
            PostModel.posted_datetime >= post_deadline
        ).all()

    @staticmethod
    def sort_posts_by_hot_score(posts):
        posts.sort(
            key=lambda p: (
                PostListService.get_hot_score_of_post(p),
                p.posted_datetime,
            ),
            reverse=True,
        )

    @staticmethod
    def paging_posts(posts, page, per_page):
        if not posts:
            return posts, 0

        number_of_pages = math.ceil(len(posts) / per_page)

        if page > number_of_pages:
            abort(
                404,
                f"Page not found, maybe over range... number of page is {number_of_pages}",
            )

        return posts[per_page * (page - 1) : per_page * page], number_of_pages

    @staticmethod
    def get_hot_score_of_post(post):
        G = 1.25
        D = PostListService.get_day_difference(post.posted_datetime)
        L = len(post.postlikes)

        return (L - 1) / pow((D + 2), G)

    @staticmethod
    def get_day_difference(date):
        return datetime.now().day - date.day

    @staticmethod
    def get_posts_with_paging(per_page, page):
        return PostListService.order_post_query_from_latest(
            PostModel.query
        ).paginate(page=page, per_page=per_page)

    @staticmethod
    def get_posts_by_gallery_with_paging(gallery, per_page, page):
        posts = PostListService.order_post_query_from_latest(
            PostModel.query.filter_by(gallery_id=gallery.gallery_id)
        ).paginate(page=page, per_page=per_page)

        return posts

    @staticmethod
    def get_posts_by_user_with_paging(user, per_page, page):
        posts = PostListService.order_post_query_from_latest(
            PostModel.query.filter_by(user_id=user.id)
        ).paginate(page=page, per_page=per_page)

        return posts

    @staticmethod
    def get_paginated_posts(
        gallery=None,
        user=None,
        page=1,
        per_page=20,
    ):
        query = PostModel.query

        if user:
            query = query.filter_by(uploader_id=user.email)

        if gallery:
            query = query.filter_by(gallery_id=gallery.id)

        paged_posts = query\
            .order_by(PostModel.posted_datetime.desc())\
            .paginate(per_page=per_page, page=page)\

        return paged_posts

    @staticmethod
    def order_post_query_from_latest(posts, reverse=False):
        o = (
            PostModel.posted_datetime.desc()
            if reverse is False
            else PostModel.posted_datetime.asc()
        )

        return posts.order_by(o)

    @classmethod
    def get_user_liked_posts(cls, user, per_page=20, page=1):
        return PostModel.query.\
            join(PostlikeModel).\
            join(UserModel).filter_by(email=user.email)\
            .order_by(PostModel.posted_datetime.desc())\
            .paginate(per_page=per_page, page=page)

    @classmethod
    def get_post_user_wrote_comment(cls, user, per_page=20, page=1):
        return PostModel.query.\
            join(CommentModel).\
            join(UserModel, CommentModel.wrote_user_id == UserModel.email).\
            filter_by(email=user.email) \
            .order_by(PostModel.posted_datetime.desc()) \
            .paginate(per_page=per_page, page=page)

