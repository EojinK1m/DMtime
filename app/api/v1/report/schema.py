from marshmallow.validate import Range, Length

from app.extensions import ma

from .model import PostReport, CommentReport
#
#
# class PostReportSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = PostReport
#
#     id = ma.auto_field()
#     reason = ma.auto_field()
#     detail_reason = ma.auto_field()
#     reported_content_type = ma.auto_field()
#     reporter = ma.Nested("UserSchema", only=["username"])
#     reported_post = ma.Nested("PostSchema", only=["title", "id", "content"])


class CommentReportSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CommentReport

    id = ma.auto_field()
    reason = ma.auto_field()
    detail_reason = ma.auto_field()
    reporter = ma.Nested("UserSchema", only=["username"])
    reported_comment = ma.Nested(
        "CommentSchema", exclude=["upper_comment_id", "wrote_datetime"]
    )


class CommentReportInputSchema(ma.Schema):
    reason = ma.Integer(required=True, validate=Range(min=1, max=10))
    detail_reason = ma.Str(required=True, validate=Length(max=500))
    comment_id = ma.Integer(required=True, allow_none=True)


class PostReportInputSchema(ma.Schema):
    reason = ma.Integer(required=True, validate=Range(min=1, max=10))
    detail_reason = ma.Str(required=True, validate=Length(max=500))
    post_id = ma.Integer(required=False, allow_none=True)



# reports_schema = ReportSchema(
#     many=True, exclude=["detail_reason", "reported_post", "reported_comment"]
# )
# comment_report_schema = ReportSchema(exclude=["reported_post"])
# post_report_schema = ReportSchema(exclude=["reported_comment"])
