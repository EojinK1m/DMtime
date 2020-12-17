from datetime import datetime

from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

from app import db

from app.api.v1.board.post.model import PostModel
from app.api.v1.board.comment.model import CommentModel,\
                                        comments_schema,\
                                        comments_schema_user,\
                                        CommentInputSchema,\
                                        CommentPatchInputSchema
from app.api.v1.user.account.model import AccountModel
from app.api.v1.user.model import UserModel


def is_correct_length(content_len):
    return content_len <= 100

def check_user_permission(comment, admin_allow):
    request_user = AccountModel.get_user_by_email(email=get_jwt_identity())

    if admin_allow:
        roles = get_jwt_claims()['roles']
        if roles == 'admin':
            return True

    return  request_user.id == comment.writer.id


class CommentService():
    
    @staticmethod
    @jwt_required
    def modify_comment(comment_id):
        comment = CommentModel.query.get(comment_id)
        json = request.get_json()

        if not comment:
            return jsonify(msg='wrong comment_id, comment not found'), 404

        if not check_user_permission(comment=comment, admin_allow=False):
            return jsonify(msg=f'access denied, u r not {comment.writer.username}'), 403

        validate_error = CommentPatchInputSchema().validate(json)
        if validate_error:
            return jsonify(msg='json validate error'), 400

        new_content = json.get('content')



        # new_content = request.json.get('content', None)
        # if not new_content:
        #     return jsonify(msg='content parameter missed'), 400
        #
        # if not is_correct_length(len(new_content)):
        #     return jsonify(msg='content is too long, it must be shorter than 100'), 413
        if new_content:
            comment.content = json.get('content')
        comment.wrote_datetime = datetime.now()

        db.session.commit()

        return jsonify(msg='comment modify succeed'), 200

    @staticmethod
    @jwt_required
    def delete_comment(comment_id):

        comment = CommentModel.query.get(comment_id)
        if not comment:
            return jsonify(msg='wrong comment_id, comment not found'), 404

        if not check_user_permission(comment=comment, admin_allow=True):
            return jsonify(msg=f'access denied, u r not {comment.writer.username}'), 403

        comment.delete_comment()
        db.session.commit()

        return jsonify(msg='delete succeed'), 200

    @staticmethod
    def abort_if_not_exist_comment_id(comment_id):
        if (CommentModel.query.get(comment_id) == None):
            abort(404, 'comment not found')

    @staticmethod
    def get_comment_by_id(comment_id):
        comment = CommentModel.query.filter_by(id=comment_id).first()
        if comment is None:
            abort(404, f'Comment{comment_id} Not Found.')

        return comment

    @staticmethod
    def check_comment_access_permission_of_account(comment, account, admin_allow):
        permission = account.user.id == comment.writer.id

        if admin_allow:
            if account.is_admin():
                permission = True

        if permission is False:
            abort(403, 'Access denied.')



class CommentListService():
    @staticmethod
    def get_comments_by_post_id_and_paging_order_by_latest(post_id, per_page, page):
        return CommentModel.query\
            .filter_by(wrote_post_id = post_id)\
            .order_by(CommentModel.wrote_datetime.desc())\
            .paginate(per_page=per_page, page=page)

    @staticmethod
    def get_comments_by_user_id_and_paging_order_by_latest(user_id, per_page, page):
        return CommentModel.query\
            .filter_by(wrote_user_id = user_id)\
            .order_by(CommentModel.wrote_datetime.desc())\
            .paginate(per_page=per_page, page=page)

    @staticmethod
    def create_comment(content,
                       is_anonymous,
                       wrote_datetime,
                       wrote_user_id,
                       wrote_post_id,
                       upper_comment_id):
        try:
            new_comment = CommentModel(
                content=content,
                is_anonymous=is_anonymous,
                wrote_datetime=wrote_datetime,
                wrote_user_id=wrote_user_id,
                wrote_post_id=wrote_post_id,
                upper_comment_id=upper_comment_id
            )

            db.session.add(new_comment)
            db.session.commit()
        except:
            abort(500, "An error occur while create comment on db.")