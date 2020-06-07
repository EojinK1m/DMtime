from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required,\
                                get_jwt_identity,\
                                get_jwt_claims

from app import db

from app.api.board.post.model import PostModel,\
                                     PostLikeModel,\
                                     posts_schema, post_schema, posts_schema_user,\
                                     PostPostInputValidateSchema,\
                                     PostPatchInputValidateSchema

from app.api.board.gallery.model import GalleryModel

from app.api.user.model import UserModel
from app.api.user.account.model import AccountModel
from app.api.image.service import ImageService

def check_user_permission(post):
    identify = get_jwt_identity()
    roles = get_jwt_claims()['roles']
    if roles == 'admin':
        return True
    user = AccountModel.query.filter_by(email=identify).first().user
    return user.id == post.uploader.id


class PostService():

    @staticmethod
    def provide_post(post_id):
        post = PostModel.query.get(post_id)

        if not post:
            return jsonify({'msg': 'Not found'}), 404

        post.increase_view()
        return jsonify(post_schema.dump(post)), 200

    @staticmethod
    @jwt_required
    def delete_post(post_id):
        post = PostModel.query.get(post_id)

        if not post:
            return jsonify({'msg': 'Not found'}), 404
        if not check_user_permission(post):
            return jsonify(msg='access denied'), 403

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

        json = request.get_json()

        validate_error = PostPatchInputValidateSchema().validate(json)
        if validate_error:
            return jsonify(msg='json validate error'), 400

        title = json.get('title', None)
        content = json.get('content', None)
        image_ids = json.get('image_ids', None)

        delete_images_ids = []
        new_images_ids = []

        if image_ids:
            if post.images:
                before_image_ids = [image.id for image in post.images]
                new_images_ids = [id for id in image_ids if not id in before_image_ids]
                delete_images_ids = [id for id in before_image_ids if not id in image_ids]
            else:
                new_images_ids = image_ids
        else:
            if post.images:
                delete_images_ids = [image.id for image in post.images]


        for image_id_to_delete in delete_images_ids:
            ImageService.delete_image(image_id_to_delete)

        for image_id_to_register in new_images_ids:
            ImageService.set_foreign_key(image_id_to_register, post.id, 'post')


        if content:
            post.content = content
        if title:
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

        postlikes = PostLikeModel.query.filter_by(post_id=post_id)
        request_user_postlike = postlikes.filter_by(liker_id=request_user.id).first()

        if (request_user_postlike):
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
    def provide_post_list():
        gallery_id = request.args.get('gallery_id', None)
        username = request.args.get('username', None)
        page = request.args.get('page', 1)
        if not page:
            page = 1

        if (gallery_id == None):
            if username:
                user = UserModel.query.filter_by(username=username).first()
                if not user:
                    return jsonify(msg='wrong username, user not found'), 404
                posts = PostModel.query.filter_by(uploader_id=user.id)
            else:
                posts = PostModel.query
        else:
            if username:
                return jsonify(msg='gallery_id and username cant be given together, u must give one of both'), 400
            if not GalleryModel.query.get(gallery_id):
                return jsonify({'msg': 'Wrong gallery id, gallery not found'}), 404
            posts = PostModel.query.filter_by(gallery_id=gallery_id)

        if page:
            try:
                page = int(page)
            except ValueError:
                return jsonify(msg='page parameter is wrong, it must be only integer char'), 400

        posts = posts.order_by(PostModel.posted_datetime.desc()). \
            paginate(per_page=3, page=page)
        if username:
            dumped_posts = posts_schema_user.dump(posts.items)
        else:
            dumped_posts = posts_schema.dump(posts.items)

        return jsonify({'posts': dumped_posts,
                        'number_of_pages': posts.pages}), 200

    @staticmethod
    @jwt_required
    def post_post(gallery_id):
        if (gallery_id == None):
            return jsonify({'msg': 'gallery_id missed'}), 400

        post_gallery = GalleryModel.query.get(gallery_id)
        if not post_gallery:
            return jsonify({'msg': 'Wrong gallery id, gallery not found'}), 404

        uploader_account = AccountModel.query.filter_by(email=get_jwt_identity()).first()


        json = request.get_json()
        validate_error =  PostPostInputValidateSchema().validate(json)
        if validate_error:
            return jsonify(msg='json validate error'), 400

        content = json.get('content', None)
        title = json.get('title', None)
        image_ids = json.get('image_ids', None)


        if not content or not title:
            return jsonify({'msg': 'missing parameter exist'}), 400

        new_post = PostModel(content=content,
                             title=title,
                             uploader=uploader_account.user,
                             gallery=post_gallery,
                             posted_datetime=datetime.now())
        db.session.add(new_post)
        db.session.flush()

        for image_id in image_ids:
            if not ImageService.set_foreign_key(image_id=image_id, key=new_post.id, location='post'):
                db.session.rollback()
                return jsonify(msg='an error occurred while registering images, plz check image ids'), 500

        db.session.commit()
        return jsonify({'msg': 'posting succeed'}), 200

