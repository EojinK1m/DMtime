from functools import update_wrapper, partial
from flask import abort
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.extentions import db
from app.api.v1.board.gallery.model import GalleryModel
from app.api.v1.user.model import UserModel


class GalleryListService:
    @staticmethod
    def get_galleries(gallery_type=None):
        gallery_query = GalleryModel.query

        if gallery_type is not None:
            gallery_query = gallery_query.filter_by(gallery_type=gallery_type)

        return gallery_query.all()

    @staticmethod
    def get_galleries_by_gallery_type(gallery_type):
        return GalleryModel.query.filter_by(gallery_type=gallery_type).all()

    @staticmethod
    def create_new_gallery(
        gallery_id, name, explain, manager_user, gallery_type
    ):
        GalleryListService.abort_if_gallery_name_exist(name)
        GalleryListService.abort_409_if_gallery_id_is_used(gallery_id)

        try:
            new_gallery = GalleryModel(
                name=name,
                explain=explain,
                manager_user_id=manager_user.email,
                gallery_id=gallery_id,
                gallery_type=gallery_type,
            )
            db.session.add(new_gallery)
        except:
            abort(500, "An error occurred while making gallery at db.")

        return new_gallery.gallery_id

    @staticmethod
    def abort_if_gallery_name_exist(name):
        if GalleryListService.is_gallery_name_exist(name):
            abort(409, "Same named gallery already exists.")

    @staticmethod
    def abort_409_if_gallery_id_is_used(gallery_id):
        if GalleryListService.is_gallery_id_used(gallery_id):
            abort(409, "Same gallery id already used.")

    @staticmethod
    def is_gallery_name_exist(name):
        return GalleryModel.query.filter_by(name=name).first() is not None

    @staticmethod
    def is_gallery_id_used(gallery_id):
        return (
            GalleryModel.query.filter_by(gallery_id=gallery_id).first()
            is not None
        )


class GalleryService:
    class gallery_manager_required:
        """
        Check what user who send request is manager of gallery.
        """

        def __init__(self, fn):
            update_wrapper(self, fn)
            self.fn = fn

        def __call__(self, *args, **kargs):
            verify_jwt_in_request()
            request_account = UserModel.get_user_by_email(get_jwt_identity())
            target_gallery = GalleryService.get_gallery_by_id(
                kargs["gallery_id"]
            )

            if (
                target_gallery.is_manager(request_account)
                or request_account.is_admin()
            ):
                return self.fn(*args, **kargs)
            else:
                abort(403)

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
        gallery = GalleryModel.query.filter_by(gallery_id=gallery_id).first()

        if gallery is None:
            abort(404, f"Gallery{gallery_id} is not found.")

        return gallery
