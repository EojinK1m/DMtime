from app import db, ma



class PostModel(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text(), nullable=True)
    uploader_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    gallery_id = db.Column(db.Integer(),db.ForeignKey('gallery.id'), nullable=False)

    def delete_post(self):
        db.session.remove(self)

class GalleryModel(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.Text, nullable=True)
    master_id = db.Column(db.Integer(), db.ForeignKey('user.id'),  nullable=True)

    posts = db.relationship('PostModel', backref='gallery')

    def delete_gallery(self):
        db.session.remove(self)

class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostModel

    id = ma.auto_field()
    uploader = ma.Nested('UserSchema', only=['username'], uselist=False)
    content = ma.auto_field()
    title = ma.auto_field()

post_schema = PostSchema()
posts_schema = PostSchema(many=True, only=["title", "uploader", "id"])

class GallerySchema(ma.SQLAlchemySchema):
    class Meta:
        model = GalleryModel

    name = ma.auto_field()
    explain = ma.auto_field()
    id = ma.auto_field()
    master = ma.Nested('UserSchema', only=['username'])


gallery_schema  = GallerySchema()
galleries_schema = GallerySchema(many=True, only=('name', 'id'))