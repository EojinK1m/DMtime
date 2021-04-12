from flask_jwt_extended import get_jwt_identity

from app import db, ma
from datetime import datetime

from marshmallow.validate import Length, Range
from ..postlike.model import PostdislikeModel, PostlikeModel


class PostModel(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    posted_datetime = db.Column(db.DateTime(), default=datetime.now())
    views = db.Column(db.Integer(), default=0)
    is_anonymous = db.Column(db.Boolean, nullable=False)

    uploader_id = db.Column(
        db.String(320),
        db.ForeignKey("user.email", ondelete="CASCADE"),
        nullable=False,
    )
    gallery_id = db.Column(
        db.String(30),
        db.ForeignKey("gallery.gallery_id", ondelete="CASCADE"),
        nullable=False,
    )

    images = db.relationship("ImageModel")
    likes = db.relationship("PostlikeModel", passive_deletes=True)
    dislikes = db.relationship("PostdislikeModel", passive_deletes=True)
    # posted_gallery = db.relationship('GalleryModel')

    @property
    def postlikes(self):
        return self.likes

    def delete_post(self):
        db.session.delete(self)

    def increase_view(self):
        self.views = self.views + 1
        db.session.flush()


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostModel

    images = ma.Method(
        serialize="get_image_ids", deserialize="get_image_ids"
    )
    id = ma.auto_field()
    uploader = ma.Method("get_uploader_with_check_anonymous")
    content = ma.auto_field()
    title = ma.auto_field()
    views = ma.auto_field()
    posted_datetime = ma.Method(
        serialize="get_abbreviated_datetime_as_string"
    )
    is_anonymous = ma.auto_field()
    number_of_likes = ma.Method(
        serialize="get_number_of_postlikes"
    )
    number_of_dislikes = ma.Method(
        serialize="get_number_of_postdislikes"
    )
    posted_gallery = ma.Nested("GallerySchema")
    number_of_comments = ma.Method(serialize="get_number_of_comments")
    whether_exist_image = ma.Method(serialize="get_whether_image_exist")
    my_reaction = ma.Method(serialize="get_user_reaction")

    def get_abbreviated_datetime_as_string(self, obj):
        def _get_abbreviated_datetime_as_string(dt):
            if not isinstance(dt, datetime):
                raise AttributeError()

            diff_from_now = datetime.now() - dt

            if diff_from_now.days >= 1:
                return f"{dt.year:04d}.{dt.month:02d}.{dt.day:02d}."
            else:
                return f"{dt.hour:02d}:{dt.minute:02d}"

        return _get_abbreviated_datetime_as_string(obj.posted_datetime)

    def get_uploader_with_check_anonymous(self, obj):
        if obj.is_anonymous:
            return {"username": "익명의 대마인"}
        else:
            from app.api.v1.user.model import UserSchema

            return UserSchema(only=["username"]).dump(obj.uploader)

    def get_image_ids(self, obj):
        list = []
        for image in obj.images:
            list.append(image.id)
        return list

    def get_number_of_postlikes(self, obj):
        return len(obj.likes)

    def get_number_of_postdislikes(self, obj):
        return len(obj.dislikes)

    def get_number_of_comments(self, obj):
        return len(obj.comments)

    def get_whether_image_exist(self, obj):
        if not obj.images:
            return False
        else:
            return True

    def get_user_reaction(self, obj):
        user_id = get_jwt_identity()

        for like in obj.likes:
            if like.liker_id == user_id:
                return 'like'

        for dislike in obj.dislikes:
            if dislike.liker_id == user_id:
                return 'dislike'

        return 'none'


class PostPostInputValidateSchema(ma.Schema):
    content = ma.Str(required=True, validate=Length(min=1))
    title = ma.Str(required=True, validate=Length(min=1, max=30))
    images = ma.List(ma.String(validate=Length(max=100), required=True))
    is_anonymous = ma.Boolean(required=True)


class PostResourceQueryParameterValidateSchema(ma.Schema):
    gallery_id = ma.String(
        data_key="gallery-id", required=True, validate=Length(min=1, max=30)
    )


class PostGetQueryParameterValidateSchema(ma.Schema):
    page = ma.Integer(required=False, validate=Range(min=1))
    per_page = ma.Integer(
        required=False, validate=Range(min=1), data_key="per-page"
    )
    username = ma.Str(required=False, validate=Length(min=2, max=20))
    gallery_id = ma.String(
        required=False, validate=Length(min=1, max=30), data_key="gallery-id"
    )


class HotPostGetQueryParameterValidateSchema(ma.Schema):
    page = ma.Integer(required=False, validate=Range(min=1))
    per_page = ma.Integer(
        required=False, validate=Range(min=1), data_key="per-page"
    )


class PostPatchInputValidateSchema(ma.Schema):
    content = ma.Str(required=False, validate=Length(min=1))
    title = ma.Str(required=False, validate=Length(min=1, max=30))
    images = ma.List(ma.String(validate=Length(max=100)), required=False)


post_schema = PostSchema(
    many=False, exclude=["whether_exist_image", "number_of_comments"]
)
posts_schema = PostSchema(many=True, exclude=["images", "content"])
posts_schema_user = PostSchema(
    many=True, exclude=["content", "images", "uploader"]
)
