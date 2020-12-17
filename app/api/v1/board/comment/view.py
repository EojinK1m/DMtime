from datetime import datetime

from flask import make_response, abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.util.request_validator import RequestValidator
from app.api.v1.board.comment.service import CommentService, CommentListService
from app.api.v1.board.comment.model import \
    comments_schema_user,\
    comments_schema,\
    CommentInputSchema,\
    PostCommentParameterSchema,\
    CommentPatchInputSchema
from app.api.v1.user.service import UserService
from app.api.v1.board.post.service import PostService
from app.api.v1.user.account.service import AccountService

class CommentList(Resource):
    def get(self):
        post_id = request.args.get('post-id', None)
        username = request.args.get('username', None)
        page = request.args.get('page', default=1, type=int)
        per_page= request.args.get('per-page', default=20, type=int)

        if post_id is not None and username is not None:
            abort(400, 'post_id and username cant be given together, u must give one of both')
        elif post_id is None and username is None:
            abort(400, 'Parameter missed')

        if post_id:
            PostService.get_post_by_post_id(post_id)
            comments = CommentListService.get_comments_by_post_id_and_paging_order_by_latest(post_id=post_id, page=page, per_page=per_page)
            dumped_comments = comments_schema.dump(comments.items)
        elif username:
            found_user = UserService.get_user_by_username(username)
            comments = CommentListService.get_comments_by_user_id_and_paging_order_by_latest(user_id=found_user.id, page=page, per_page=per_page)
            dumped_comments = comments_schema_user.dump(comments.items)

        return {'comments':dumped_comments,
                'number_of_pages':comments.pages}, 200

    @jwt_required
    def post(self):

        def validate_request():
            RequestValidator.validate_request(PostCommentParameterSchema(), request.args)
            RequestValidator.validate_request(CommentInputSchema(), request.json)

        def check_comment_belonging_to_this_post(comment, post):
            if comment.wrote_post_id != post.id:
                abort(400, 'Comment is not belonging to post.')

        validate_request()

        request_account = AccountService.find_account_by_email(email=get_jwt_identity())
        json = request.json
        upper_comment_id = json.get('upper_comment_id', None)
        is_anonymous = json.get('is_anonymous')
        content = json.get('content')
        post_id = request.args.get('post-id')

        target_post = PostService.get_post_by_post_id(post_id=post_id)

        if upper_comment_id is not None:
            upper_comment = CommentService.get_comment_by_id(upper_comment_id)
            check_comment_belonging_to_this_post(comment=upper_comment, post=target_post)

        CommentListService.create_comment(
            wrote_post_id=target_post.id,
            wrote_datetime=datetime.now(),
            wrote_user_id=request_account.user.id,
            content=content,
            upper_comment_id=upper_comment_id,
            is_anonymous=is_anonymous
        )

        return {}, 200


class Comment(Resource):
    @jwt_required
    def patch(self, comment_id):
        json = request.json
        RequestValidator.validate_request(CommentPatchInputSchema(), json)

        comment = CommentService.get_comment_by_id(comment_id)
        request_account = AccountService.find_account_by_email(email=get_jwt_identity())

        CommentService.check_comment_access_permission_of_account(comment=comment, account=request_account)

        new_content = json.get('content', None)
        if new_content is None:
            new_content = comment.content

        CommentService.modify_comment(
            comment=comment,
            new_content=new_content
        )

        return {}, 200

    def delete(self, comment_id):
        return make_response(CommentService.delete_comment(comment_id))
