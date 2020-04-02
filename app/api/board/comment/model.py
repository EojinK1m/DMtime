from app import db, ma


class CommentModel(db.Model):
    __tablename__ = 'comment'

    id  = db.Column(db.Integer(), primary_key=True)
    write_user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    wrote_post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
    wrote_comment_id = db.Column(db.Integer(), db.ForeignKey('comment.id'), nullable=True)
    content = db.Column(db.String(100), nullable=False)
    wrote_datetime = db.Column(db.DateTime(), nullable=False)

    writer = db.relationship('UserModel')


class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CommentModel

    id = ma.auto_field()
    content = ma.auto_field()
    wrote_datetime = ma.auto_field()
    wrote_comment_id = ma.auto_field()
    writer = ma.Nested('UserSchema', only=['username'])


comments_schema = CommentSchema(many=True)