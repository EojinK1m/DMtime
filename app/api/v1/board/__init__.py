from flask import Blueprint
from flask_restful import Api

from app.api.v1.board.post.view import Post, PostList, HotPostList, PostLike
from app.api.v1.board.gallery import Gallery, GalleryList
from app.api.v1.board.gallery import Report, ReportList
from app.api.v1.board.comment.view import Comment, CommentList

board_blueprint = Blueprint('board', 'board_blueprint')
board_api = Api(board_blueprint)


board_api.add_resource(Post, '/posts/<post_id>')
board_api.add_resource(PostLike, '/posts/<post_id>/like')
board_api.add_resource(PostList, '/posts')
board_api.add_resource(HotPostList, '/posts/hot')


board_api.add_resource(Gallery, '/galleries/<gallery_id>')
board_api.add_resource(GalleryList, '/galleries')

board_api.add_resource(Comment, '/comments/<comment_id>')
board_api.add_resource(CommentList, '/comments')

board_api.add_resource(Report, '/galleries/<gallery_id>/reports/<report_id>')
board_api.add_resource(ReportList, '//galleries/<gallery_id>/reports')
