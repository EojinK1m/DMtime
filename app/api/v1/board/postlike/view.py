from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.api.v1.board.post.service import PostService

class PostLike(Resource):
    @jwt_required
    def post(self, post_id):
        post = PostService.get_post_by_post_id(post_id)
        request_account = AccountService.find_user_by_email(get_jwt_identity())

        postlike = PostLikeService.get_postlike_by_post_and_account(
            post=post, account=request_account
        )

        if postlike:
            PostLikeService.delete_postlike(postlike)
            message = "Cancel post like"
        else:
            PostLikeService.create_postlike(account=request_account, post=post)
            message = "Like post"

        db.session.commit()
        return {"message": message, "likes": len(post.postlikes)}, 201

    @jwt_required
    def delete(self, post_id):
        pass


class PostDislike(Resource):
    def post(self, post_id):
        pass
    
    @jwt_required
    def delete(self, post_id):
        pass