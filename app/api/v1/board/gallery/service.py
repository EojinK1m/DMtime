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
    def modify_gallery_info(gallery, name, explain):
        GalleryListService.abort_if_gallery_name_exist(name)
        gallery.patch(name=name, explain=explain)

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
