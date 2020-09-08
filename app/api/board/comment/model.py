from app import db, ma


class CommentModel(db.Model):
    __tablename__ = 'comment'

    id  = db.Column(db.Integer(), primary_key=True)
    wrote_user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    wrote_post_id = db.Column(db.Integer(), db.ForeignKey('post.id', ondelete="SET NULL"), nullable=True)
    upper_comment_id = db.Column(db.Integer(), db.ForeignKey('comment.id', ondelete="SET NULL"), nullable=True)
    content = db.Column(db.String(100), nullable=False)
    wrote_datetime = db.Column(db.DateTime(), nullable=False)
    is_anonymous = db.Column(db.Boolean, nullable=False)

    writer = db.relationship('UserModel', backref='comments')
    wrote_post = db.relationship('PostModel', backref='comments')

    def delete_comment(self):
        db.session.delete(self)

class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CommentModel

    id = ma.auto_field()
    content = ma.auto_field()
    wrote_datetime = ma.auto_field()
    upper_comment_id = ma.auto_field()
    writer = ma.Nested('UserSchema', only=['username'])
    wrote_post = ma.Nested('PostSchema', only=['id'])

from marshmallow.validate import Length

class CommentInputSchema(ma.Schema):
    content = ma.Str(required = True, validate = Length(min = 1, max = 100))
    upper_comment_id = ma.Integer(required = False, allow_none = True)


class CommentPatchInputSchema(ma.Schema):
    content = ma.Str(required = False, validate = Length(min = 1, max = 100))




comments_schema = CommentSchema(many=True, exclude=['wrote_post'])
comments_schema_user = CommentSchema(many=True, exclude=['writer', 'upper_comment_id'])
