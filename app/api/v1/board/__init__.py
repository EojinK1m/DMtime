from flask_restful import Api

from app.api.v1.board.post.view import Post, PostList, HotPostList, PostLike
from app.api.v1.board.gallery.view import Gallery, GalleryList
from app.api.v1.board.gallery.report.view import Report, ReportList
from app.api.v1.board.comment.view import Comment, CommentList


board_api = Api()

board_api.add_resource(Post, "/board/posts/<post_id>")
board_api.add_resource(PostLike, "/board/posts/<post_id>/like")
board_api.add_resource(PostList, "/board/posts")
board_api.add_resource(HotPostList, "/board/posts/hot")

board_api.add_resource(Gallery, "/board/galleries/<gallery_id>")
board_api.add_resource(GalleryList, "/board/galleries")

board_api.add_resource(Comment, "/board/comments/<comment_id>")
board_api.add_resource(CommentList, "/board/comments")

board_api.add_resource(Report, "/board/galleries/<gallery_id>/reports/<report_id>")
board_api.add_resource(ReportList, "/board/galleries/<gallery_id>/reports")
