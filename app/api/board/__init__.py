from flask import Blueprint
from flask_restful import Api

from app.api.board.view import Post, PostList, PostLike,\
                                Gallery, GalleryList

from app.api.board.comment.view import Comment, CommentList

board_blueprint = Blueprint('board', 'board_blueprint')
board_api = Api(board_blueprint)


board_api.add_resource(Post, '/post/<post_id>')
board_api.add_resource(PostLike, '/post/<post_id>/like')
board_api.add_resource(PostList, '/post')

board_api.add_resource(Gallery, '/gallery/<gallery_id>')
board_api.add_resource(GalleryList, '/gallery')

board_api.add_resource(Comment, '/comment/<comment_id>')
board_api.add_resource(CommentList, '/comment')
