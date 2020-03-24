from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.api.user.model import UserModel, user_schema
from app.api.user.account.model import AccountModel

class UserService:


    @staticmethod
    def provide_user_info(username):
        find_user = UserModel.query.filter_by(username=username).first()
        if not find_user:
            return jsonify({'msg':'user not found'}), 404

        print(find_user.username)
        from app.api.board.model import PostSchema

        posts = PostSchema(many=True, only=['title', 'id']).dump(find_user.posts)
        return jsonify(user_schema.dump(find_user),posts), 200


    @staticmethod
    @jwt_required
    def modify_user_info(username, data):
        new_username = data.get('username', None)
        new_explain = data.get('user_explain', None)
        new_profile_image = data.get('profile_image', None)


        if not new_username or new_explain or new_profile_image:
            return jsonify({'msg': 'parameter missed '}), 402

        user = (AccountModel.query.filter_by(email=get_jwt_identity()).first()).user
        if not user:
            return jsonify({'msg': 'user not found'}), 404
        elif user.username != username:
            return jsonify({'msg':f'access denied, you are not {user.username}'}), 403

        user.username = new_username
        user.profile_image = new_profile_image
        user.explain = new_explain
        db.session.commit()

        return jsonify({'msg':'modification succeed'}), 200
