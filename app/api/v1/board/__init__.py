from flask_restful import Api

from app.api.v1.board.post.view import Post, PostList, HotPostList
from app.api.v1.board.gallery.view import Gallery, GalleryList
from .report.view import CommentReport, CommentReports, CommentReportsNestedInGallery
from app.api.v1.board.gallery.report.view import Report, ReportList
from app.api.v1.board.comment.view import Comment, CommentList
from app.api.v1.board.postlike.view import PostLike, PostDislike

board_api = Api()

resource_routes = {
    "/board/posts/<post_id>": Post,
    "/board/posts/<post_id>/like": PostLike,
    "/board/posts/<post_id>/dislike": PostDislike,
    "/board/posts": PostList,
    "/board/posts/hot": HotPostList,
    "/board/galleries/<gallery_id>": Gallery,
    "/board/galleries": GalleryList,
    "/board/comments/<comment_id>": Comment,
    "/board/comments": CommentList,
    "/board/galleries/<gallery_id>/reports/<report_id>": Report,
    "/board/galleries/<gallery_id>/comment-reports": CommentReportsNestedInGallery,
    "/comment-reports/<report_id>": CommentReport,
    "/comment-reports": CommentReports
}

for path, resource in resource_routes.items():
    board_api.add_resource(resource, path)
