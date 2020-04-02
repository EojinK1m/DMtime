from flask import make_response
from flask_restful import Resource
from app.api.board.comment.service import CommentService, CommentListService



class CommentList(Resource):
    def get(self):
        return make_response(CommentListService.provide_comments())
    def post(self):
        return make_response(CommentListService.write_comment())

class Comment(Resource):
    pass