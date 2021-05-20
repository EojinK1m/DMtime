from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.util.request_validator import RequestValidator

from app.api.v1.board.postlike.service import (
    PostdislikeService,
    PostlikeService
)
from app.api.v1.user.service import UserService
from app.api.v1.board.postlike.schema import (
    RequestPostlikeApiQueryParameterValidateSchema
)


def validate_post_id(post_id):
    RequestValidator.validate_request(
        data={"post_id": post_id},
        schema=RequestPostlikeApiQueryParameterValidateSchema()
    )


class PostLike(Resource):

    def __init__(self, *args, **kwargs):
        self.postlike_service = PostlikeService()
        self.postdislike_service = PostdislikeService()
        
    #     self.postlike_service = kwargs["post_like_service"]
    #     self.reuqest_validator = kwargs.get('request_validator')
    #     self.post_id_validate_schema = kwargs.get('post_id_validate_schema')
    # def get_user_from_jwt()

    @jwt_required
    def post(self, post_id):
        request_user = UserService.get_user_by_email_or_none(get_jwt_identity())
        validate_post_id(post_id)

        self.postlike_service.abort_409_if_postlike_exists(
            user_id=request_user.email,
            post_id=post_id
        )
        self.postdislike_service.abort_409_if_postdislike_exists(
            user_id=request_user.email,
            post_id=post_id
        )

        self.postlike_service.create_postlike(
            post_id=post_id,
            user_id=request_user.email
        )

        number_of_likes = \
            len(self.postlike_service.get_postlikes_by_post_id(post_id))

        return {"number_of_likes": number_of_likes}, 201

        '''
            validate_post_id

            check_postlike_or_postdislike_already_exist
                if exist abort 409
            
            create postlike by user
            response 201, number_of_likes
        '''

    @jwt_required
    def delete(self, post_id):
        request_user = UserService.get_user_by_email_or_none(get_jwt_identity())
        validate_post_id(post_id)

        postlike_to_delete = \
            self.postlike_service.get_postlike_or_abort_404(
                user_id=request_user.email,
                post_id=post_id
            )
        
        postlike_to_delete.delete()

        number_of_likes = \
            len(self.postlike_service.get_postlikes_by_post_id(post_id))

        return {"number_of_likes": number_of_likes}, 200
        '''
            validate_post_id

            check_is_postlike_by_request_user_exist
                if not exist abort 404
                else get postlike
            
            delete postlike
            
            response 200, number_of_likes
        '''
        pass


class PostDislike(Resource):
    
    def __init__(self, *args, **kwargs):
        self.postdislike_service = PostdislikeService()
        self.postlike_service = PostlikeService()

    @jwt_required
    def post(self, post_id):
        request_user = UserService.get_user_by_email_or_none(get_jwt_identity())
        validate_post_id(post_id)

        self.postlike_service.abort_409_if_postlike_exists(
            user_id=request_user.email,
            post_id=post_id
        )
        self.postdislike_service.abort_409_if_postdislike_exists(
            user_id=request_user.email,
            post_id=post_id
        )

        self.postdislike_service.create_postdislike(
            post_id=post_id,
            user_id=request_user.email
        )

        number_of_dislikes = \
            len(self.postdislike_service.get_postdislikes_by_post_id(post_id))

        return {"number_of_dislikes": number_of_dislikes}, 201


        '''
            validate_post_id

            check_postlike_or_postdislike_already_exist
                if exist abort 409
            
            create postlike by user
            response 201, number_of_likes
        '''
        pass
    
    @jwt_required
    def delete(self, post_id):
        request_user = UserService.get_user_by_email_or_none(get_jwt_identity())
        validate_post_id(post_id)

        postdislike_to_delete = \
            self.postdislike_service.get_postdislike_or_abort_404(
                user_id=request_user.email,
                post_id=post_id
            )
        
        postdislike_to_delete.delete()

        number_of_dislikes = \
            len(self.postdislike_service.get_postdislikes_by_post_id(post_id))

        return {"number_of_dislikes": number_of_dislikes}, 200

        '''
            validate_post_id

            check_is_postlike_by_request_user_exist
                if not exist abort 404
                else get postlike
            
            delete postlike
            
            response 200, number_of_likes
        '''
        pass