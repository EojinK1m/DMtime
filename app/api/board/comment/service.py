from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

from app import db

from app.api.board.post.model import PostModel
from app.api.board.comment.model import CommentModel,\
                                        comments_schema,\
                                        comments_schema_user,\
                                        CommentInputSchema,\
                                        CommentPatchInputSchema
from app.api.user.account.model import AccountModel
from app.api.user.model import UserModel

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


class CommentListService():


    @staticmethod
    @jwt_required
    def write_comment():
        post_id = request.args.get('post-id', None)
        if not post_id:
            return jsonify(msg='post_id missed'), 400
        if not PostModel.query.get(post_id):
            return jsonify(msg='wrong post_id, post not found'), 404

        json = request.get_json()
        error = CommentInputSchema().validate(json)
        if error:
            return jsonify(msg='json validate error'), 400

        content = json.get('content', None)
        upper_comment_id = json.get('upper_comment_id')

        if upper_comment_id:
            upper_comment = CommentModel.query.get(upper_comment_id)
            if not upper_comment:
                return jsonify(msg='upper comment is not found'), 404

            if not upper_comment.wrote_post_id == int(post_id):
                return jsonify(msg='post_id of upper_comment is not same with post_id that received'), 403

        # if not content:
        #     return jsonify(msg='content parameter missed'), 400
        # if not is_correct_length(len(content)):
        #     return jsonify(msg='content is too long, it must be shorter than 100'), 413


        writer = AccountModel.query.filter_by(email = get_jwt_identity()).first().user

        new_comment = CommentModel(content=content,
                                   wrote_datetime=datetime.now(),
                                   wrote_user_id=writer.id,
                                   wrote_post_id=post_id,
                                   upper_comment_id=upper_comment_id)
        db.session.add(new_comment)
        db.session.commit()

        return jsonify(msg='comment successfully wrote'), 200



    @staticmethod
    def provide_comments():
        post_id = request.args.get('post-id', None)
        username = request.args.get('username', None)
        page = request.args.get('page', None)
        per_page= request.args.get('per-page', None)

        if not page:
            page = 1
        if not per_page:
            per_page = 50

        if post_id:
            if username:
                return jsonify(msg='post_id and username cant be given together, u must give one of both'), 400
            else:
                if not PostModel.query.get(post_id):
                    return jsonify(msg=f'wrong post_id, post {post_id} not found'), 404
                comments = CommentModel.query.filter_by(wrote_post_id = post_id)
        elif username:
            found_user = UserModel.query.filter_by(username=username).first()
            if not found_user:
                return jsonify(msg=f'wrong username, user {username} not found'), 404
            comments = CommentModel.query.filter_by(wrote_user_id = found_user.id)
        else:
            return jsonify(msg='parameter missed'), 400

        if page:
             try: page = int(page)
             except ValueError: return jsonify(msg='page parameter is wrong, it must be only integer char'), 400

        if page:
             try: per_page = int(per_page)
             except ValueError: return jsonify(msg='per-page parameter is wrong, it must be only integer char'), 400

        comments = comments.order_by(CommentModel.wrote_datetime.desc()).\
               paginate(per_page=per_page, page=page)

        if username:
            dumped_comments = comments_schema_user.dump(comments.items)
        else:
            dumped_comments = comments_schema.dump(comments.items)

        return jsonify(comments=dumped_comments,
                       msg='query_succeed',
                       number_of_pages=comments.pages), 200
