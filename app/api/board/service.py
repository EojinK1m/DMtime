from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db

from app.api.board.model import PostModel, post_schema, posts_schema,\
    GalleryModel, gallery_schema, galleries_schema


from app.api.user.account.model import AccountModel


class PostService():


    @staticmethod
    def provide_post(post_id):
        post = PostModel.query.get(post_id)

        if not post:
            return jsonify({'msg':'Not found'}), 404

        return jsonify(post_schema.dump(post)), 200



class PostListService():


    @staticmethod
    def provide_post_list(gallery_id):

        if (gallery_id == None):
            posts = PostModel.query.all()
        else:
            if not GalleryModel.query.get(gallery_id):
                return jsonify({'msg':'Wrong gallery id'}), 404

            posts = PostModel.query.filter_by(gallery = gallery_id)


        return jsonify(posts_schema.dump(posts)), 200

    @staticmethod
    @jwt_required
    def post_post(gallery_id, data):
        if(gallery_id == None):
            return jsonify({'msg':'gallery_id missed'}), 400
        post_gallery = GalleryModel.query.get(gallery_id)
        if not post_gallery:
            return jsonify({'msg': 'Wrong gallery id'}), 404

        content = data.get('content', None)
        title = data.get('title', None)
        uploader_account = AccountModel.query.filter_by(email=get_jwt_identity()).first()

        if not content or not title:
            return jsonify({'msg':'missing parameter exist'}), 400

        new_post = PostModel(content=content,
                             title=title,
                             uploader=uploader_account.user,
                             gallery=post_gallery)

        db.session.add(new_post)
        db.session.commit()

        return jsonify({'msg':'posting succeed'}), 200


class GalleryListService:


    @staticmethod
    def provide_gallery_list():
        return jsonify(galleries_schema.dump(GalleryModel.query.all())), 200

    @staticmethod
    @jwt_required
    def create_gallery(data):
        name = data.get('name', None)
        explain = data.get('explain', None)
        master_account = AccountModel.query.filter_by(email=get_jwt_identity()).first()

        if not name or not explain:
            return jsonify({'msg':'missing parameter exist'}), 400

        if GalleryModel.query.filter_by(name=name).first():
            return jsonify({'msg':'same named gallery exist'}), 403

        new_gallery = GalleryModel(name=name,
                                   explain=explain,
                                   master=master_account.user)

        db.session.add(new_gallery)
        db.session.commit()

        return jsonify({'msg':'successfully gallery created'}), 200


class GalleryService:


    @staticmethod
    def provide_gallery_info(gallery_id):
        gallery = GalleryModel.query.get(gallery_id)

        if not gallery:
            return jsonify({'msg':'gallery not fount'}), 404

        return jsonify(gallery_schema.dump(gallery)), 200

