from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db

from app.api.board.model import PostModel, post_schema, posts_schema,\
    GalleryModel, gallery_schema, galleries_schema


from app.api.user.account.model import AccountModel
from app.api.image.service import ImageService


class PostService():


    @staticmethod
    def provide_post(post_id):
        post = PostModel.query.get(post_id)

        if not post:
            return jsonify({'msg':'Not found'}), 404

        post.increase_view()
        return jsonify(post_schema.dump(post)), 200



class PostListService():


    @staticmethod
    def provide_post_list(gallery_id):

        if (gallery_id == None):
            posts = PostModel.query.all()
        else:
            if not GalleryModel.query.get(gallery_id):
                return jsonify({'msg':'Wrong gallery id, gallery not found'}), 404

            posts = PostModel.query.filter_by(gallery_id = gallery_id)


        return jsonify(posts_schema.dump(posts)), 200

    @staticmethod
    @jwt_required
    def post_post(gallery_id, data):
        if(gallery_id == None):
            return jsonify({'msg':'gallery_id missed'}), 400
        post_gallery = GalleryModel.query.get(gallery_id)
        if not post_gallery:
            return jsonify({'msg': 'Wrong gallery id, gallery not found'}), 404

        content = data.get('content', None)
        title = data.get('title', None)
        image_ids = data.get('image_ids', None)

        uploader_account = AccountModel.query.filter_by(email=get_jwt_identity()).first()

        if not content or not title:
            return jsonify({'msg':'missing parameter exist'}), 400


        new_post = PostModel(content=content,
                             title=title,
                             uploader=uploader_account.user,
                             gallery=post_gallery)

        db.session.add(new_post)
        db.session.flush()

        if image_ids:
            for image_id in image_ids:
                if not ImageService.set_foreign_key(image_id=image_id, key=new_post.id, location='post'):
                    db.session.rollback()
                    return jsonify(msg='an error occurred while registering images, plz check image ids'), 500

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

        try:
            new_gallery = GalleryModel(name=name,
                                       explain=explain,
                                       master=master_account.user)

            db.session.add(new_gallery)
        except:
            return jsonify(msg='an error occurred while making gallery at db'), 500
        db.session.commit()
        return jsonify({'msg':'successfully gallery created'}), 200


class GalleryService:


    @staticmethod
    def provide_gallery_info(gallery_id):
        gallery = GalleryModel.query.get(gallery_id)

        if not gallery:
            return jsonify({'msg':'gallery not fount'}), 404

        return jsonify(gallery_schema.dump(gallery)), 200

    @staticmethod
    @jwt_required
    def delete_gallery(gallery_id):
        gallery = GalleryModel.query.get(gallery_id)

        if not gallery:
            return jsonify(msg='gallery not found'), 404

        delete_user = AccountModel.query.get(get_jwt_identity())
        if not delete_user:
            return jsonify(msg='unknown user, user cant found')
        if not delete_user.id == gallery.master_id:
            return jsonify(msg='access denied'), 403

        for post in gallery.posts:
            post.delete_post()
        gallery.delete_gallery()

