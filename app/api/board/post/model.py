from app import db, ma
from datetime import datetime

from marshmallow.validate import Length

class PostModel(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text(), nullable=True) #sould be false
    posted_datetime = db.Column(db.DateTime(), default=datetime.now())
    views = db.Column(db.Integer(), default=0)
    is_anonymous = db.Column(db.Boolean, nullable=False)


    uploader_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    gallery_id = db.Column(db.Integer(),db.ForeignKey('gallery.id', ondelete='CASCADE'), nullable=False)

    images = db.relationship('ImageModel')
    postlikes = db.relationship('PostLikeModel', passive_deletes=True)
    posted_gallery = db.relationship('GalleryModel')

    def delete_post(self):
        db.session.delete(self)

    def increase_view(self):
        self.views = self.views + 1
        db.session.commit()



class PostLikeModel(db.Model):
    __tablename__ = 'postlike'

    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    liker_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

from app.api.board.gallery.model import GalleryModel

class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostModel

    image_ids = ma.Method(serialize='get_image_ids', deserialize='get_image_ids')
    id = ma.auto_field()
    uploader = ma.Nested('UserSchema', only=['username'], uselist=False)
    content = ma.auto_field()
    title = ma.auto_field()
    views = ma.auto_field()
    posted_datetime = ma.auto_field()
    likes = ma.Method(serialize='get_number_of_postlikes', deserialize='get_number_of_postlikes')
    posted_gallery = ma.Nested('GallerySchema', only=['name', 'id'])
    number_of_comments = ma.Method(serialize='get_number_of_comments')
    whether_exist_image = ma.Method(serialize = 'get_whether_image_exist')

    def get_image_ids(self, obj):
        list = []
        for image in obj.images:
            list.append(image.id)
        return list

    def get_number_of_postlikes(self, obj):
        return len(obj.postlikes)

    def get_number_of_comments(self, obj):
        return len(obj.comments)

    def get_whether_image_exist(self, obj):
        if not obj.images:
            return False
        else:
            return True


class PostPostInputValidateSchema(ma.Schema):
    content = ma.Str(required = True, validate = Length(min = 1))
    title = ma.Str(required = True, validate = Length(min = 1, max = 30))
    image_ids = ma.List(ma.Integer, required = True)
    is_anonymous = ma.Boolean(required=True)

class PostPatchInputValidateSchema(ma.Schema):
    content = ma.Str(required = False, validate = Length(min = 1))
    title = ma.Str(required = False, validate = Length(min = 1, max = 30))
    image_ids = ma.List(ma.Integer, required = False)

post_schema = PostSchema(many=False, exclude=['whether_exist_image', 'number_of_comments'])
posts_schema = PostSchema(many=True, exclude=['posted_gallery', 'image_ids', 'content'])
posts_schema_user = PostSchema(many=True, exclude=['content', 'image_ids', 'uploader'])

