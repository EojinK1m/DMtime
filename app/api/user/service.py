from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.api.user.model import UserModel, user_schema
from app.api.user.account.model import AccountModel

class UserService:


    @staticmethod
    def provide_user_info(username): # 유저가 쓴 글도 보내주가ㅣ
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
        if not new_username:
            return jsonify({'msg': 'username parameter missed '}), 402

        user = (AccountModel.query.filter_by(email=get_jwt_identity()).first()).user
        if not user:
            return jsonify({'msg': 'user not found'}), 404
        elif user.username != username:
            return jsonify({'msg':f'access denied, you are not {user.username}'}), 403

        user.username = new_username
        db.session.commit()

        return jsonify({'msg':'modification succeed'}), 200
