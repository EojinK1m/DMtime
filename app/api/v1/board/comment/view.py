from flask import make_response, abort, request
from flask_restful import Resource
from app.api.v1.board.comment.service import CommentService, CommentListService
from app.api.v1.board.comment.model import comments_schema_user, comments_schema
from app.api.v1.user.service import UserService
from app.api.v1.board.post.service import PostService

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



    def post(self):
        return make_response(CommentListService.write_comment())

class Comment(Resource):
    def patch(self, comment_id):
        return make_response(CommentService.modify_comment(comment_id))
    def delete(self, comment_id):
        return make_response(CommentService.delete_comment(comment_id))
