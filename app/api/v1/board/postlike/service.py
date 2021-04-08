from flask import abort

from app import db

from app.api.v1.board.postlike.model import PostlikeModel, PostdislikeModel


class PostlikeService():
    def __init__(self):
        self.postlike_repository = PostlikeRepository()

    @classmethod
    def get_postlike(cls, user_id, post_id):
        return PostlikeModel.query\
            .filter_by(liker_id=user_id)\
            .filter_by(post_id=post_id)\
            .first()
    
    @classmethod
    def get_postlike_or_abort_404(cls, user_id, post_id):
        postlike = cls.get_postlike(user_id, post_id)

        if postlike is None:
            abort(404)
        
        return postlike
            
    @classmethod
    def get_postlikes_by_post_id(cls, post_id):
        return PostlikeModel.query.filter_by(post_id=post_id).all()
        # return self.postlike_repository.get_postlikes_by_post_id(post_id)

    @classmethod
    def abort_404_if_not_exist_postlike_by_user_on_post(cls, user_id, post_id):
        if cls.get_postlike(user_id, post_id) is None:
            abort(404)

    @classmethod
    def abort_409_if_postlike_exists(cls, user_id, post_id):
        if cls.get_postlike(user_id, post_id):
            abort(409)

    @classmethod
    def create_postlike(cls, user_id, post_id):
        new_postlike = PostlikeModel(
            liker_id=user_id,
            post_id=post_id
        )

        db.session.add(new_postlike)
        return new_postlike


class PostdislikeService():

    @classmethod
    def get_postdislike(cls, user_id, post_id):
        return PostdislikeModel.query\
            .filter_by(liker_id=user_id)\
            .filter_by(post_id=post_id)\
            .first()
    

    @classmethod
    def get_postdislike_or_abort_404(cls, user_id, post_id):
        postdislike = cls.get_postdislike(user_id, post_id)

        if postdislike is None:
            abort(404)
        
        return postdislike
    
    @classmethod
    def get_postdislikes_by_post_id(cls, post_id):
        return PostdislikeModel.query.filter_by(post_id=post_id).all()

    @classmethod
    def abort_409_if_postdislike_exists(cls, user_id, post_id):
        if cls.get_postdislike(user_id, post_id):
            abort(409)

    @classmethod
    def create_postdislike(cls, user_id, post_id):
        new_postdislike = PostdislikeModel(
            liker_id=user_id,
            post_id=post_id
        )

        db.session.add(new_postdislike)
        
        return new_postdislike
