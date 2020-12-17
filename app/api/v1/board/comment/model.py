from marshmallow.validate import Length, Range
from datetime import datetime

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

    report = db.relationship('ReportModel', backref='reported_comment')

    def delete_comment(self):
        db.session.delete(self)

class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CommentModel

    id = ma.auto_field()
    content = ma.auto_field()
    wrote_datetime = ma.Method('get_abbreviated_datetime_as_string')
    upper_comment_id = ma.auto_field()
    writer = ma.Method('get_writer_username_with_check_anonymous')
    is_anonymous = ma.auto_field()
    wrote_post = ma.Nested('PostSchema', only=['id'])

    def get_abbreviated_datetime_as_string(self, obj):

        def _get_abbreviated_datetime_as_string(dt):
            if not isinstance(dt, datetime):
                raise AttributeError()

            diff_from_now = datetime.now() - dt

            if diff_from_now.days >= 1:
                return f'{dt.year:04d}.{dt.month:02d}.{dt.day:02d}.'
            else:
                return f'{dt.hour:02d}:{dt.minute:02d}'

        return _get_abbreviated_datetime_as_string(obj.wrote_datetime)

    def get_writer_username_with_check_anonymous(self, obj):
        if(obj.is_anonymous):
            return {'username':'익명의 대마인'}
        else:
            from app.api.v1.user.model import UserSchema
            return UserSchema(only=['username']).dump(obj.writer)


class CommentInputSchema(ma.Schema):
    content = ma.Str(required = True, validate = Length(min = 1, max = 100))
    upper_comment_id = ma.Integer(required = False, allow_none = True)
    is_anonymous = ma.Boolean(required=True)
    

class CommentPatchInputSchema(ma.Schema):
    content = ma.Str(required = False, validate = Length(min = 1, max = 100))


class GetCommentParameterSchema(ma.Schema):
   post_id = ma.Integer(data_key="post-id", required=False)
   username = ma.Str(required=False)
   page = ma.Integer(required=False, validate=Range(min=0))
   per_page = ma.Integer(data_key="per-page", required=False, validate=Range(min=1))


class PostCommentParameterSchema(ma.Schema):
    post_id = ma.Integer(data_key="post-id", required = True)


comments_schema = CommentSchema(many=True, exclude=['wrote_post'])
comments_schema_user = CommentSchema(many=True, exclude=['writer', 'upper_comment_id'])
