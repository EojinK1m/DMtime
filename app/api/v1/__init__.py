from flask.blueprints import Blueprint
from flask_restful import Api

from .post.view import (
    Post,
    PostList,
    HotPostList,
    PostListUserLiked,
    PostListRequestUserLiked,
    PostListUserWroteComment,
    PostListRequestUserWroteComment
)
from .gallery.view import (
    Gallery,
    GalleryList
)
from .report.view import (
    CommentReport, 
    CommentReports, 
    CommentReportsNestedInGallery
)
from .comment.view import (
    Comment, 
    CommentList
)
from .postlike.view import (
    PostLike, 
    PostDislike
)
from .image.view import (
    ImageUpload, 
    Image
)
from .user.view import (
    User,
    Users,
    Account,
    AccountPassword,
    DuplicateCheckEmail,
    DuplicateCheckUsername,
    Me
)
from app.api.v1.auth.view import (
    Token,
    EmailVerificationCode
)
from app.api.v1.general import view


v1_blueprint = Blueprint("api_v1", "api_v1")

v1_blueprint.after_request(view.commit_session_after_request)
v1_blueprint.teardown_request(view.rollback_session_when_error)


users_url = "/users"
user_url = users_url + "/<username>"
account_url = user_url + "/account"

user_api_routes = {
    User: user_url,
    Users: users_url,
    DuplicateCheckUsername: users_url + "/username-duplication",
    DuplicateCheckEmail: users_url + "/email-duplication",
    Account: account_url,
    AccountPassword: account_url + '/password'
}

board_api_routes = {
    "/board/posts/<post_id>": Post,
    "/board/posts/<post_id>/like": PostLike,
    "/board/posts/<post_id>/dislike": PostDislike,
    "/board/posts": PostList,
    "/board/posts/hot": HotPostList,
    "/board/galleries/<gallery_id>": Gallery,
    "/board/galleries": GalleryList,
    "/board/comments/<comment_id>": Comment,
    "/board/comments": CommentList,
    "/board/galleries/<gallery_id>/comment-reports": CommentReportsNestedInGallery,
    "/comment-reports/<report_id>": CommentReport,
    "/comment-reports": CommentReports,
    "/users/<username>/liked-posts": PostListUserLiked,
    "/users/<username>/posts-wrote-comment": PostListUserWroteComment,
    "/me/liked-posts": PostListRequestUserLiked,
    "/me/posts-wrote-comment": PostListRequestUserWroteComment,
}

user_api = Api()
for resource, route in user_api_routes.items():
    user_api.add_resource(resource, route)

board_api = Api()
for path, resource in board_api_routes.items():
    board_api.add_resource(resource, path)

image_api = Api()
image_api.add_resource(ImageUpload, "/images")
image_api.add_resource(Image, "/images/<id>")

auth_api = Api()
auth_api.add_resource(Token, "/token")
auth_api.add_resource(EmailVerificationCode, "/email-verification-code")


board_api.init_app(v1_blueprint)
user_api.init_app(v1_blueprint)
image_api.init_app(v1_blueprint)
auth_api.init_app(v1_blueprint)

#
# gallery_list_url = '/galleries'
# gallery_url = gallery_list_url + '/<gallery_id>'
#
# me_url = "/me"
# post_list_request_user_liked_posts_url = me_url + "/liked-posts"
# post_list_request_user_wrote_comment_url = me_url + '/posts-wrote-comment'
#
# post_list_url = "/posts"
# post_list_on_gallery_url = gallery_list_url + '/posts'
# post_list_user_liked_posts_url = user_url + "/liked-posts"
# post_list_user_wrote_comment_url = user_url + '/posts-wrote-comment'
#
# post_url = post_list_url + '/<post_id>'
# post_like_url = post_url + '/like'
# post_dislike_url = post_url + "/dislike"
#
# comment_list_on_post_url = post_url + "/comments"
# comment_list_url = "/comments"
# comment_url = comment_list_url + "/<comment_id>"
#
# me_api = Api(prefix=me_url)
# post_api = Api(prefix=post_list_url)
# gallery_api = Api(prefix=gallery_list_url)
# comment_api = Api(prefix=comment_url)
#
#
# user_api.add_resource(Users)
# user_api.add_resource(User, user_url)
# user_api.add_resource(Account, account_url)
# user_api.add_resource(AccountPassword, password_url)
# user_api.add_resource(DuplicateCheckEmail, email_duplication_url)
# user_api.add_resource(DuplicateCheckUsername, username_duplication_url)
#
# me_api.add_resource(Me)
# me_api.add_resource(PostListRequestUserLiked, post_list_request_user_liked_posts_url)
# me_api.add_resource(PostListRequestUserWroteComment, post_list_request_user_wrote_comment_url)