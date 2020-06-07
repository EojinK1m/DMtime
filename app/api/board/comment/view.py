from flask import make_response
from flask_restful import Resource
from app.api.board.comment.service import CommentService, CommentListService



class CommentList(Resource):
    def get(self):
        return make_response(CommentListService.provide_comments())
    def post(self):
        return make_response(CommentListService.write_comment())

class Comment(Resource):
    def patch(self, comment_id):
        return make_response(CommentService.modify_comment(comment_id))
    def delete(self, comment_id):
        return make_response(CommentService.delete_comment(comment_id))
