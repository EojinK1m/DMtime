from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db

from app.api.board.model import PostModel
from app.api.board.comment.model import CommentModel, comments_schema
from app.api.user.account.model import AccountModel
from app.api.user.model import UserModel

def is_correct_length(content_len):
    return content_len <= 100


class CommentService():


    @staticmethod
    @jwt_required
    def modify_comment(comment_id):
        comment = CommentModel.query.get(comment_id)
        if not comment:
            return jsonify(msg='wrong comment_id, comment not found'), 404

        modify_user = AccountModel.get_user_by_email(email=get_jwt_identity())

        if not modify_user.id == comment.writer.id:
            return jsonify(msg=f'access denied, u r not {comment.writer.username}'), 403

        new_content = request.json.get('content', None)
        if not new_content:
            return jsonify(msg='content parameter missed'), 400

        if not is_correct_length(len(new_content)):
            return jsonify(msg='content is too long, it must be shorter than 100'), 413

        comment.content = new_content
        comment.wrote_datetime = datetime.now()

        db.session.commit()

        return jsonify(msg='comment modify succeed'), 200

    @staticmethod
    @jwt_required
    def delete_comment(comment_id):
        comment = CommentModel.query.get(comment_id)
        if not comment:
            return jsonify(msg='wrong comment_id, comment not found'), 404

        delete_user = AccountModel.get_user_by_email(get_jwt_identity())
        if not delete_user.id == comment.writer.id:
            return jsonify(msg=f'access denied, u r not {comment.writer.username}'), 403

        comment.delete_comment()
        db.session.commit()

        return jsonify(msg='delete succeed'), 200


class CommentListService():


    @staticmethod
    @jwt_required
    def write_comment():
        post_id = request.args.get('post_id', None)
        if not post_id:
            return jsonify(msg='post_id missed'), 400
        if not PostModel.query.get(post_id):
            return jsonify(msg='wrong post_id, post not found'), 404


        content = request.json.get('content', None)
        if not content:
            return jsonify(msg='content parameter missed'), 400
        if not is_correct_length(len(content)):
            return jsonify(msg='content is too long, it must be shorter than 100'), 413


        writer = AccountModel.query.filter_by(email = get_jwt_identity()).first().user

        new_comment = CommentModel(content=content,
                                   wrote_datetime=datetime.now(),
                                   wrote_user_id=writer.id)

        upper_comment_id = request.args.get('upper_comment_id', None)
        if upper_comment_id:
            upper_comment = CommentModel.query.get(upper_comment_id)
            if not upper_comment:
                return jsonify(msg='upper comment is not found'), 404
            if not upper_comment.wrote_post_id == post_id:
                return jsonify(msg='post_id of upper_comment is not same with post_id that received'), 403

            new_comment.upper_comment_id = upper_comment_id
        new_comment.wrote_post_id = post_id

        db.session.add(new_comment)
        db.session.commit()

        return jsonify(msg='comment successfully wrote'), 200



    @staticmethod
    def provide_comments():
        post_id = request.args.get('post_id', None)
        username = request.args.get('username', None)

        if post_id:
            if username:
                return jsonify(msg='post_id and username cant be given together, u must give one of both'), 400
            else:
                comments = CommentModel.query.filter_by(wrote_post_id = post_id)
        elif username:
            found_user = UserModel.query.filter_by(username=username).first()
            if not found_user:
                return jsonify(msg=f'wrong username user {username} not found'), 404
            comments = found_user.comments
        else:
            return jsonify(msg='parameter missed'), 400

        return jsonify({'comments':comments_schema.dump(comments),
                       'msg':'query_succeed'}), 200
