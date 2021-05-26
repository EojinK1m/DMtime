from flask import abort

from app.extensions import db

from app.api.v1.comment.model import CommentModel


class CommentService:
    @staticmethod
    def modify_comment(comment, new_content):
        comment.content = new_content
        db.session.commit()

    @staticmethod
    def delete_comment(comment):
        comment.delete_comment()
        db.session.commit()

    @staticmethod
    def abort_if_not_exist_comment_id(comment_id):
        if CommentModel.query.get(comment_id) == None:
            abort(404, "comment not found")

    @staticmethod
    def get_comment_by_id(comment_id):
        comment = CommentModel.query.filter_by(id=comment_id).first()
        if comment is None:
            abort(404, f"Comment{comment_id} Not Found.")

        return comment

    @staticmethod
    def check_comment_access_permission_of_account(
        comment, account, admin_allow=False
    ):
        permission = account.email == comment.writer.email

        if admin_allow:
            if account.is_admin():
                permission = True

        if permission is False:
            abort(403, "Access denied.")


class CommentListService:

    @staticmethod
    def get_paginated_comments(
        post=None,
        user=None,
        page=1,
        per_page=20,
    ):
        query = CommentModel.query

        if post:
            query = query.filter_by(wrote_post_id=post.id)
        if user:
            query = query.filter_by(wrote_user_id=user.email)

        paged_comments = query\
            .order_by(CommentModel.wrote_datetime.desc())\
            .paginate(per_page=per_page, page=page)\

        return paged_comments

    @staticmethod
    def create_comment(
        content,
        is_anonymous,
        wrote_datetime,
        wrote_user_id,
        wrote_post_id,
        upper_comment_id,
    ):
        try:
            new_comment = CommentModel(
                content=content,
                is_anonymous=is_anonymous,
                wrote_datetime=wrote_datetime,
                wrote_user_id=wrote_user_id,
                wrote_post_id=wrote_post_id,
                upper_comment_id=upper_comment_id,
            )

            db.session.add(new_comment)
            db.session.commit()
        except:
            abort(500, "An error occur while create comment on db.")
