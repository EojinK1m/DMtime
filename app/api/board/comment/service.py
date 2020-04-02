from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db

from app.api.board.model import PostModel
from app.api.board.comment.model import CommentModel, comments_schema
from app.api.user.account.model import AccountModel


class CommentService():
    pass

class CommentListService():


    @staticmethod
    @jwt_required
    def write_comment():
        post_id = request.args.get('post_id', None)
        if not post_id:
            return jsonify(msg='post_id missed'), 400
        if not PostModel.query.get(post_id):
            return jsonify(msg='wrong post_id, post not found'), 404
        post_id = int(post_id)


        content = request.json.get('content', None)
        if not content:
            return jsonify(msg='content parameter missed'), 400
        if len(content) > 100:
            return jsonify(msg='content is too long, it must be shorter than 100'), 413


        writer = AccountModel.query.filter_by(email = get_jwt_identity()).first().user

        new_comment = CommentModel(content=content,
                                   wrote_datetime=datetime.now(),
                                   write_user_id=writer.id)

        upper_comment_id = request.args.get('upper_comment_id', None)
        if upper_comment_id:
            upper_comment = CommentModel.query.get(upper_comment_id)
            if not upper_comment:
                return jsonify(msg='upper comment is not found'), 404
            if not upper_comment.wrote_post_id == post_id:
                return jsonify(msg='post_id of upper_comment is not same with post_id that received'), 403

            new_comment.wrote_comment_id = upper_comment_id
        new_comment.wrote_post_id = post_id

        db.session.add(new_comment)
        db.session.commit()

        return jsonify(msg='comment successfully wrote'), 200



    @staticmethod
    def provide_comments():
        post_id = request.args.get('post_id', None)
        comments = CommentModel.query.filter_by(wrote_post_id = post_id)


        return jsonify({'comments':comments_schema.dump(comments),
                       'msg':'query_succeed'}), 200
