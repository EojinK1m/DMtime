from flask_restful import Resource
from flask_jwt_extended import jwt_required

class PostLike(Resource):
    @jwt_required
    def post(self, post_id):
        '''
            validate_post_id

            check_postlike_or_postdislike_already_exist
                if exist abort 404
            
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
    def post(self, post_id):
        '''
            validate_post_id

            check_postlike_or_postdislike_already_exist
                if exist abort 404
            
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