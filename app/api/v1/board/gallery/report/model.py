import enum
from marshmallow.validate import Length, Range

from app import db, ma


class ReportModel(db.Model):
    __tablename__ = "report"

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Integer(), nullable=False)
    detail_reason = db.Column(db.String(500), nullable=False)
    reported_user_id = db.Column(
        db.String(320),
        db.ForeignKey("user.email", ondelete="CASCADE"),
        nullable=False,
    )
    gallery_id = db.Column(
        db.Integer(),
        db.ForeignKey("gallery.id", ondelete="CASCADE"),
        nullable=False,
    )
    reported_content_type = db.Column(db.Integer(), nullable=False)
    post_id = db.Column(
        db.Integer(),
        db.ForeignKey("post.id", ondelete="SET NULL"),
        nullable=True,
    )
    comment_id = db.Column(
        db.Integer(),
        db.ForeignKey("comment.id", ondelete="SET NULL"),
        nullable=True,
    )

    reporter = db.relationship("UserModel")
    reported_post = db.relationship("PostModel")

    def delete_report(self):
        db.session.delete(self)

    def add_report(self):
        db.session.add(self)


class Reason(enum.Enum):
    PRONOGRAPHY = 1
    SLANDER = 2
    PLASTER = 3
    AD = 4


class ContentType(enum.Enum):
    POST = 1
    COMMENT = 2


class ReportSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReportModel

    id = ma.auto_field()
    reason = ma.auto_field()
    detail_reason = ma.auto_field()
    reported_content_type = ma.auto_field()
    reporter = ma.Nested("UserSchema", only=["username"])
    reported_post = ma.Nested("PostSchema", only=["title", "id", "content"])
    reported_comment = ma.Nested(
        "CommentSchema", exclude=["upper_comment_id", "wrote_datetime"]
    )


class ReportInputSchema(ma.Schema):
    reason = ma.Integer(required=True, validate=Range(min=1, max=10))
    detail_reason = ma.Str(required=True, validate=Length(max=500))
    reported_content_type = ma.Integer(
        required=True, validate=Range(min=1, max=2)
    )
    post_id = ma.Integer(required=False, allow_none=True)
    comment_id = ma.Integer(required=False, allow_none=True)


class ReportPostInputSchema(ma.Schema):
    reason = ma.Integer(required=True, validate=Range(min=1, max=10))
    detail_reason = ma.Str(required=True, validate=Length(max=500))
    reported_content_type = ma.Integer(
        required=True, validate=Range(min=1, max=2)
    )
    post_id = ma.Integer(required=True, allow_none=False)
    comment_id = ma.Integer(required=False, allow_none=True)


class ReportCommentInputSchema(ma.Schema):
    reason = ma.Integer(required=True, validate=Range(min=1, max=10))
    detail_reason = ma.Str(required=True, validate=Length(max=500))
    reported_content_type = ma.Integer(
        required=True, validate=Range(min=1, max=2)
    )
    post_id = ma.Integer(required=False, allow_none=True)
    comment_id = ma.Integer(required=True)


reports_schema = ReportSchema(
    many=True, exclude=["detail_reason", "reported_post", "reported_comment"]
)
comment_report_schema = ReportSchema(exclude=["reported_post"])
post_report_schema = ReportSchema(exclude=["reported_comment"])
