from app import db, ma


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(16), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), unique=True)
    explain = db.Column(db.Text, nullable=True)

    posts = db.relationship('PostModel', backref='uploader')
    profile_image = db.relationship('ImageModel', uselist=False)
    managing_gallery = db.relationship('GalleryModel', backref='manager')
    def delete_user(self):
        db.session.delete(self)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel()


    username = ma.auto_field()
    explain = ma.auto_field()
    profile_image = ma.Nested('ImageSchema', only=["url", "id"])


user_schema = UserSchema()
users_schema = UserSchema(many=True, only=['username', 'profile_image'])

from marshmallow import validate

class UserPatchInputSchema(ma.Schema):
    username = ma.Str(required = False, validate = validate.Length(min = 2, max = 20))
    user_explain = ma.Str(required = False, validate = validate.Length(max = 400))
    profile_image_id = ma.Int(required = False, allow_null = True)

class UserPutInputSchema(ma.Schema):
    username = ma.Str(required = True, validate = validate.Length(min = 2, max = 20))
    user_explain = ma.Str(required = True, validate = validate.Length(max = 400))
    profile_image_id = ma.Int(required = False, allow_null = True)