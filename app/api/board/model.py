from app import db, ma
from datetime import datetime

class PostModel(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text(), nullable=True) #sould be false
    posted_datetime = db.Column(db.DateTime(), default=datetime.now())
    views = db.Column(db.Integer(), default=0)
    images = db.relationship('ImageModel')
    postlikes = db.relationship('PostLikeModel')
    posted_gallery = db.relationship('GalleryModel')

    uploader_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    gallery_id = db.Column(db.Integer(),db.ForeignKey('gallery.id'), nullable=False)


    def delete_post(self):
        db.session.delete(self)

    def increase_view(self):
        self.views = self.views + 1
        db.session.commit()



class PostLikeModel(db.Model):
    __tablename__ = 'postlike'

    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
    liker_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)



class GalleryModel(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.Text, nullable=True)
    master_id = db.Column(db.Integer(), db.ForeignKey('user.id'),  nullable=True)

    posts = db.relationship('PostModel', backref='gallery')

    def delete_gallery(self):
        db.session.delete(self)


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

post_schema = PostSchema(many=False, exclude=['whether_exist_image', 'number_of_comments'])
posts_schema = PostSchema(many=True, exclude=['posted_gallery', 'image_ids', 'content'])
posts_schema_user = PostSchema(many=True, exclude=['content', 'image_ids', 'uploader'])


class GallerySchema(ma.SQLAlchemySchema):
    class Meta:
        model = GalleryModel

    name = ma.auto_field()
    explain = ma.auto_field()
    id = ma.auto_field()
    master = ma.Nested('UserSchema', only=['username'])


gallery_schema  = GallerySchema()
galleries_schema = GallerySchema(many=True, only=('name', 'id'))