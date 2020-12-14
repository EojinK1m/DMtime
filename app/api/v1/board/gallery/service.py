from functools import update_wrapper, partial
from werkzeug.exceptions import Forbidden
from flask import jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from app import db


from app.api.v1.board.gallery.model import gallery_schema,\
                                        GalleryModel,\
                                        galleries_schema,\
                                        GalleryPatchValidateSchema,\
                                        GalleryPostValidateSchema


from app.api.v1.user.account.model import AccountModel


class GalleryListService:


    @staticmethod
    def provide_gallery_list():
        return jsonify(msg = 'query succeed',
                       galleries = galleries_schema.dump(GalleryModel.query.all())), 200


    @staticmethod
    @jwt_required
    def create_gallery(data):
        e = GalleryPostValidateSchema().validate(data)
        if e:
            return jsonify(msg='json validate error'), 400

        name = data.get('name', None)
        explain = data.get('explain', None)
        creating_user = AccountModel.get_user_by_email(get_jwt_identity())

        if GalleryModel.query.filter_by(name=name).first():
            return jsonify({'msg':'same named gallery exist'}), 403

        try:
            new_gallery = GalleryModel(name=name,
                                       explain=explain,
                                       manager_user_id=creating_user.id)

            db.session.add(new_gallery)
        except:
            return jsonify(msg='an error occurred while making gallery at db'), 500
        db.session.commit()
        return jsonify({'msg':'successfully gallery created'}), 200


    @staticmethod
    def get_galleries():
        return GalleryModel.query.all()

    @staticmethod
    def create_new_gallery(name, explain, manager_user):
        GalleryListService.abort_if_gallery_name_exist(name)

        try:
            new_gallery = GalleryModel(name=name,
                                       explain=explain,
                                       manager_user_id=manager_user.id)

            db.session.add(new_gallery)
            db.session.commit()
        except:
            abort (500, 'An error occurred while making gallery at db.')

        return new_gallery.id

    @staticmethod
    def abort_if_gallery_name_exist(name):
        if(GalleryListService.is_gallery_name_exist(name)):
            abort(409, 'Same named gallery exist.')

    @staticmethod
    def is_gallery_name_exist(name):
        return GalleryModel.query.filter_by(name=name).first() is not None


class GalleryService:
    
    class gallery_manager_required:
        '''
        Check what user who send request is manager of gallery.
        '''
        def __init__(self, fn):
            update_wrapper(self, fn)
            self.fn = fn
        

        def __call__(self, *args, **kargs):
            verify_jwt_in_request()
            request_account = AccountModel.get_account_by_email(get_jwt_identity())
            target_gallery = GalleryService.get_gallery_by_id(kargs['gallery_id'])

            if(target_gallery.is_manager(request_account.user) or request_account.is_admin()):
                return self.fn(*args, **kargs)
            else:
                raise Forbidden()
        

        def __get__(self, instance, owner=None):
            return partial(self.__call__, instance)


    @staticmethod
    def provide_gallery_info(gallery_id):
        gallery = GalleryModel.query.get(gallery_id)

        if not gallery:
            return jsonify({'msg':'gallery not fount'}), 404

        return jsonify(msg = 'query succeed',
                       gallery = gallery_schema.dump(gallery)), 200

    @staticmethod
    @gallery_manager_required
    def modify_gallery_info(gallery_id):
        gallery = GalleryModel.query.get(gallery_id)
        if not gallery:
            return jsonify({'msg': 'gallery not fount'}), 404
 
        json = request.get_json()

        e = GalleryPatchValidateSchema().validate(json)
        if e:
            return jsonify(msg='json validate error'), 400

        explain = json.get('explain', None)
        name = json.get('name', None)

        if GalleryModel.query.filter_by(name=name).first():
            return jsonify({'msg':'same named gallery exist'}), 409

        if explain:
            gallery.explain = explain
        if name:
            gallery.name = name

        db.session.commit()
        return jsonify(msg='modify succeed'), 200



    @staticmethod
    def delete_gallery(gallery):
        try:
            gallery.delete_gallery()
            db.session.commit()
        except:
            abort(500)

    @staticmethod
    def is_exist_gallery_id(gallery_id):
        return GalleryService.get_gallery_by_id(gallery_id) != None

    @staticmethod
    def get_gallery_by_id(gallery_id):
        gallery = GalleryModel.query.filter_by(id=gallery_id).first()

        if gallery is None:
            abort(404, '')

        return gallery
