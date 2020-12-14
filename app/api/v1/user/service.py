from flask import jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.api.v1.user.model import UserModel, user_schema
from app.api.v1.user.account.model import AccountModel

from app.api.v1.image.service import ImageService

class UserService:


    @staticmethod
    def provide_user_info(username):
        find_user = UserModel.query.filter_by(username=username).first()
        if not find_user:
            return jsonify({'msg':'user not found'}), 404

        return jsonify({'msg':'query succeed',\
                        'user_info':user_schema.dump(find_user)})

    @staticmethod
    def get_user_by_username(username):
        find_user = UserModel.query.filter_by(username=username).first()
        if find_user is None:
            abort(404, 'User not found')

        return find_user

    @staticmethod
    @jwt_required
    def modify_user_info(username, data):
        from app.api.v1.user.model import UserPatchInputSchema
        error = UserPatchInputSchema().validate(data)
        if error:
            return jsonify(msg= 'Bad request, json body is wrong'), 400

        user = (AccountModel.query.filter_by(email=get_jwt_identity()).first()).user
        if not user or not UserModel.query.filter_by(username=username).first():
            return jsonify({'msg': 'user not found'}), 404
        elif user.username != username:
            return jsonify({'msg': f'access denied, you are not {username}'}), 403

        new_username = data.get('username', None)
        new_explain = data.get('user_explain', None)
        new_profile_image_id = data.get('profile_image_id',
                                        user.profile_image.id if user.profile_image else None)


        if not (new_username == None):
            if(UserModel.query.filter_by(username=new_username).first()):
                return jsonify(msg='Bad request, same username exist'), 400
            user.username = new_username
        if not (new_explain == None):
            user.explain = new_explain
        if not UserService.set_profile_image(user, new_profile_image_id):
            return jsonify({'msg': f'image not found, image {new_profile_image_id}is not exist'}), 404

        db.session.commit()

        return jsonify({'msg':'modification succeed'}), 200

    @staticmethod
    def set_profile_image(user, profile_image_id):
        print(user.id)
        print(profile_image_id)


        if user.profile_image == None:
            if profile_image_id == None:
                return True
        elif user.profile_image.id == profile_image_id:
            return True

        if user.profile_image:
            if not ImageService.delete_image(user.profile_image.id):
                return False
        if profile_image_id:
            if not ImageService.set_foreign_key(profile_image_id, user.id, 'user'):
                return False

        return True

    @staticmethod
    def delete_user(user):
        profile_image = user.profile_image

        if profile_image:
            ImageService.delete_image(profile_image.id)
        user.delete_user()





