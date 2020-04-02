from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db

from app.api.board.model import PostModel, post_schema, posts_schema,\
    GalleryModel, gallery_schema, galleries_schema,\
    PostLikeModel


from app.api.user.account.model import AccountModel
from app.api.image.service import ImageService


def check_user_permission(post):
    user = AccountModel.query.filter_by(email=get_jwt_identity()).first().user
    return user.id == post.uploader.id



class PostService():


    @staticmethod
    def provide_post(post_id):
        post = PostModel.query.get(post_id)

        if not post:
            return jsonify({'msg':'Not found'}), 404

        post.increase_view()
        return jsonify(post_schema.dump(post)), 200

    @staticmethod
    @jwt_required
    def delete_post(post_id):
        post = PostModel.query.get(post_id)

        if not post:
            return jsonify({'msg':'Not found'}), 404
        if not check_user_permission(post):
            return jsonify(msg='access denied'), 403

        for image in post.images:
            ImageService.delete_image(image.id)
        post.delete_post()

        db.session.commit()
        return jsonify(msg='post deleted'), 200


    @staticmethod
    @jwt_required
    def modify_post(post_id):
        post = PostModel.query.get(post_id)
        if not post:
            return jsonify(msg='Not found'), 404
        if not check_user_permission(post):
            return jsonify(msg='access denied'), 403

        json_data = request.json
        title = json_data.get('title', None)
        content = json_data.get('content', None)
        image_ids = json_data.get('image_ids', None)

        before_image_ids = [image.id for image in post.images]
        delete_images_ids= [id for id in before_image_ids if not id in image_ids]
        new_image_ids = [id for id in image_ids if not id in before_image_ids]

        for image_id_to_delete in delete_images_ids:
            ImageService.delete_image(image_id_to_delete)
        for image_id_to_register in new_image_ids:
            ImageService.set_foreign_key(image_id_to_register, post.id, 'post')

        if not title or not content:
            return jsonify(msg='parameter missed'), 400

        post.content = content
        post.title = title

        db.session.commit()
        return jsonify(msg='modify succeed'), 200


    @staticmethod
    @jwt_required
    def post_like(post_id):
        post = PostModel.query.get(post_id)
        request_user = AccountModel.query.filter_by(email=get_jwt_identity()).first().user

        if not post:
            return 404

        postlikes = PostLikeModel.query.filter_by(post_id = post_id)
        request_user_postlike = postlikes.filter_by(liker_id=request_user.id).first()
        
        if(request_user_postlike):
            db.session.delete(request_user_postlike)
            db.session.commit()

            return jsonify(msg='cancel post like'), 200
        else:
            new_postlike = PostLikeModel(liker_id=request_user.id, post_id=post.id)
            db.session.add(new_postlike)
            db.session.commit()

            return jsonify(msg='post like'), 201










class PostListService():


    @staticmethod
    def provide_post_list(gallery_id, page):

        if (gallery_id == None):
            posts = PostModel.query.all()
        else:
            if not GalleryModel.query.get(gallery_id):
                return jsonify({'msg':'Wrong gallery id, gallery not found'}), 404
            posts = PostModel.query.filter_by(gallery_id=gallery_id)

        if page:
             page = int(page)

        posts = posts.order_by(PostModel.posted_datetime.desc()).\
                paginate(per_page=3, page=page)

        return jsonify({'posts':posts_schema.dump(posts.items),
                       'number_of_pages':posts.pages}), 200

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
        image_ids = data.get('image_ids', None)

        uploader_account = AccountModel.query.filter_by(email=get_jwt_identity()).first()

        if not content or not title:
            return jsonify({'msg':'missing parameter exist'}), 400


        new_post = PostModel(content=content,
                             title=title,
                             uploader=uploader_account.user,
                             gallery=post_gallery,
                             posted_datetime=datetime.now())

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
    def modify_gallery_info(gallery_id):
        gallery = GalleryModel.query.get(gallery_id)
        if not gallery:
            return jsonify({'msg': 'gallery not fount'}), 404
        json_info = request.json
        explain = json_info.get('explain', None)
        name = json_info.get('name', None)
        if not name:
            return jsonify(msg='name parameter missed'), 403

        gallery.explain = explain
        gallery.name = name

        db.session.commit()
        return jsonify(msg='modify succeed'), 200



    @staticmethod
    @jwt_required
    def delete_gallery(gallery_id):
        gallery = GalleryModel.query.get(gallery_id)

        if not gallery:
            return jsonify(msg='gallery not found'), 404

        delete_user = (AccountModel.query.filter_by(email=get_jwt_identity()).first()).user
        if not delete_user:
            return jsonify(msg='unknown user, user cant found')
        if not delete_user.id == gallery.master_id:
            return jsonify(msg='access denied'), 403

        for post in gallery.posts:
            post.delete_post()
        gallery.delete_gallery()

        db.session.commit()
        return jsonify(msg='gallery deleted'), 200
