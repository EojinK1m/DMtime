from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.util.request_validator import RequestValidator

from app.api.v1.board.postlike.service import (
    PostdislikeService,
    PostlikeService
)
from app.api.v1.user.service import UserService
from app.api.v1.board.postlike.schema import (
    RequestPostlikeApiQueryParameterVaidateSchema
)

class PostLike(Resource):

    def __init__(self, *args, **kwargs):
        self.postlike_service = PostlikeService()
    #     self.postlike_service = kwargs["post_like_service"]
    #     self.reuqest_validator = kwargs.get('request_validator')
    #     self.post_id_validate_schema = kwargs.get('post_id_validate_schema')

    def validate_post_id(self, post_id):
        RequestValidator.validate_request(
            data={"post_id": post_id},
            schema=RequestPostlikeApiQueryParameterVaidateSchema()
        )
    # def get_user_from_jwt()

    @jwt_required
    def post(self, post_id):
        request_user = UserService.get_user_by_email_or_none(get_jwt_identity())
        self.validate_post_id(post_id)
        
        if self.postlike_service.get_postlike_by_user_id(request_user.email):
            abort(409)
        
        self.postlike_service.create_postlike(request_user.email)
        number_of_likes = \
            len(self.postlike_service.get_postlikes_by_post_id(post_id))

        return {number_of_likes: number_of_likes}, 201

        '''
            validate_post_id

            check_postlike_or_postdislike_already_exist
                if exist abort 409
            
            create postlike by user
            response 201, number_of_likes
        '''

    @jwt_required
    def delete(self, post_id):
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
    
    def validaet_post_id(post_id):
        pass    

    @jwt_required
    def post(self, post_id):
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
        '''
            validate_post_id

            check_is_postlike_by_request_user_exist
                if not exist abort 404
                else get postlike
            
            delete postlike
            
            response 200, number_of_likes
        '''
        pass