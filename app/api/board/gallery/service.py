from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app import admin_required, db


from app.api.board.gallery.model import gallery_schema, GalleryModel, galleries_schema
from app.api.user.account.model import AccountModel


class GalleryListService:


    @staticmethod
    def provide_gallery_list():
        return jsonify(galleries_schema.dump(GalleryModel.query.all())), 200

    @staticmethod
    @admin_required
    def create_gallery(data):
        name = data.get('name', None)
        explain = data.get('explain', None)

        if not name or not explain:
            return jsonify({'msg':'missing parameter exist'}), 400

        if GalleryModel.query.filter_by(name=name).first():
            return jsonify({'msg':'same named gallery exist'}), 403

        try:
            new_gallery = GalleryModel(name=name,
                                       explain=explain)

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
    @admin_required
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
    @admin_required
    def delete_gallery(gallery_id):
        gallery = GalleryModel.query.get(gallery_id)

        if not gallery:
            return jsonify(msg='gallery not found'), 404

        delete_user = (AccountModel.query.filter_by(email=get_jwt_identity()).first()).user
        if not delete_user:
            return jsonify(msg='unknown user, user cant found')
        if not delete_user.id == gallery.master_id:
            return jsonify(msg='access denied'), 403

        gallery.delete_gallery()

        db.session.commit()
        return jsonify(msg='gallery deleted'), 200