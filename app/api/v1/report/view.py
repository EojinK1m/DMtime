from functools import update_wrapper, partial

from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.util.request_validator import RequestValidator

from .service import CommentReportService, CommentReportListService
from .schema import CommentReportSchema, CommentReportInputSchema

from ..gallery.service import GalleryService
from ..comment.service import CommentService

from app.api.v1.auth.service import TokenService
from app.api.v1.general.service import admin_required


def permission_required(fn):
    @jwt_required
    def wraps(*args, **kwargs):
        report_id = kwargs['report_id']

        target_report = CommentReportService.get_report_by_id(report_id)
        request_user = TokenService.get_user_from_token()

        if not(
            request_user.is_admin() or
            target_report.nested_gallery.is_manager(request_user)
        ):
            abort(403)

        return fn(*args, **kwargs)

    update_wrapper(wraps, fn)
    return wraps


class CommentReport(Resource):
    @permission_required
    def get(self, report_id):
        return CommentReportSchema().\
            dumps(CommentReportService.get_report_by_id(report_id))

    @permission_required
    def delete(self, report_id):
        report_2_delete = CommentReportService.get_report_by_id(report_id)
        report_2_delete.delete()

        return {}, 200


class CommentReports(Resource):
    @admin_required
    def get(self):
        comment_reports = CommentReportListService.get_all_comment_reports()

        return CommentReportSchema(many=True).dumps(comment_reports)

    @jwt_required
    def post(self):
        RequestValidator.validate_request(CommentReportInputSchema(), request.json)

        request_data = request.json

        request_user = TokenService.get_user_from_token()
        comment_to_report = CommentService.get_comment_by_id(request_data['comment_id'])

        CommentReportListService.create_new_report(
            comment=comment_to_report,
            reason=request_data['reason'],
            detail_reason=request_data['detail_reason'],
            reporter=request_user
        )

        return {}, 201


class CommentReportsNestedInGallery(Resource):
    @GalleryService.gallery_manager_required
    def get(self, gallery_id):
        gallery = GalleryService.get_gallery_by_id(gallery_id)
        comment_reports = \
            CommentReportListService.get_comment_reports_in_gallery(gallery)

        return CommentReportSchema(many=True).dumps(comment_reports)

# class ReportList(Resource):
#     @GalleryService.gallery_manager_required
#     def get(self, gallery_id):
#         reports = reports_schema.dump(
#             ReportListService.get_reports_by_gallery_id(gallery_id)
#         )
#
#         return reports, 200
#
#     @jwt_required
#     def post(self, gallery_id):
#         request_account = AccountService.find_user_by_email(get_jwt_identity())
#         create_report_data = self.validate_json_body(request.json)
#
#         self.check_reported_write_is_exist(create_report_data)
#         GalleryService.get_gallery_by_id(gallery_id)
#
#         ReportListService.create_new_report(
#             reporter=request_account,
#             reported_content_type=create_report_data["reported_content_type"],
#             reason=create_report_data["reason"],
#             detail_reason=create_report_data["detail_reason"],
#             comment_id=create_report_data.get("comment_id"),
#             post_id=create_report_data.get("post_id"),
#             gallery_id=gallery_id,
#         )
#
#         return {}, 201
#
#     def validate_json_body(self, json):
#         RequestValidator.validate_request(ReportInputSchema(), json)
#
#         content_type = json["reported_content_type"]
#         if content_type == ContentType.POST.value:
#             validate_schema = ReportPostInputSchema()
#         elif content_type == ContentType.COMMENT.value:
#             validate_schema = ReportCommentInputSchema()
#
#         RequestValidator.validate_request(validate_schema, json)
#
#         if json.get("comment_id") and json.get("post_id"):
#             abort(400, "comment id and post id can be together")
#
#         return json
#
#     def check_reported_write_is_exist(self, json):
#         if json["reported_content_type"] == ContentType.POST.value:
#             PostService.abort_if_not_exist_post_id(json["post_id"])
#         elif json["reported_content_type"] == ContentType.COMMENT.value:
#             CommentService.abort_if_not_exist_comment_id(json["comment_id"])
#
#
# class PostReport(Resource):
#     @GalleryService.gallery_manager_required
#     def get(self, gallery_id, report_id):
#         return self.dump_report(PostReport.get_report_by_id(report_id))
#
#     def dump_report(self, report):
#         content_type = report.reported_content_type
#
#         if content_type == ContentType.COMMENT.value:
#             return comment_report_schema.dump(report)
#         elif content_type == ContentType.POST.value:
#             return post_report_schema.dump(report)
#         else:
#             abort(500)
#
#     @GalleryService.gallery_manager_required
#     def delete(self, gallery_id, report_id):
#         return ReportService.delete_report(report_id)
#
#
# class PostReportList(Resource):
#     @GalleryService.gallery_manager_required
#     def get(self, gallery_id):
#         reports = reports_schema.dump(
#             ReportListService.get_reports_by_gallery_id(gallery_id)
#         )
#
#         return reports, 200
#
#     @jwt_required
#     def post(self, gallery_id):
#         request_account = AccountService.find_user_by_email(get_jwt_identity())
#         create_report_data = self.validate_json_body(request.json)
#
#         self.check_reported_write_is_exist(create_report_data)
#         GalleryService.get_gallery_by_id(gallery_id)
#
#         ReportListService.create_new_report(
#             reporter=request_account,
#             reported_content_type=create_report_data["reported_content_type"],
#             reason=create_report_data["reason"],
#             detail_reason=create_report_data["detail_reason"],
#             comment_id=create_report_data.get("comment_id"),
#             post_id=create_report_data.get("post_id"),
#             gallery_id=gallery_id,
#         )
#
#         return {}, 201
#
#     def validate_json_body(self, json):
#         RequestValidator.validate_request(ReportInputSchema(), json)
#
#         content_type = json["reported_content_type"]
#         if content_type == ContentType.POST.value:
#             validate_schema = ReportPostInputSchema()
#         elif content_type == ContentType.COMMENT.value:
#             validate_schema = ReportCommentInputSchema()
#
#         RequestValidator.validate_request(validate_schema, json)
#
#         if json.get("comment_id") and json.get("post_id"):
#             abort(400, "comment id and post id can be together")
#
#         return json
#
#     def check_reported_write_is_exist(self, json):
#         if json["reported_content_type"] == ContentType.POST.value:
#             PostService.abort_if_not_exist_post_id(json["post_id"])
#         elif json["reported_content_type"] == ContentType.COMMENT.value:
#             CommentService.abort_if_not_exist_comment_id(json["comment_id"])
#
#
# class PostReportListIncludedGallery(Resource):
#     pass
#
#
# class CommentReportListIncludedGallery(Resource):
#     pass
