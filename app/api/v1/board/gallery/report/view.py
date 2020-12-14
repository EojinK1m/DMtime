from flask import make_response, request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.util.request_validator import RequestValidator

from app.api.v1.board.gallery.report.service import ReportService, ReportListService
from app.api.v1.board.gallery.report.model import \
    ContentType,\
    ReportPostInputSchema,\
    ReportCommentInputSchema,\
    ReportInputSchema,\
    reports_schema,\
    comment_report_schema,\
    post_report_schema

from app.api.v1.board.gallery.service import GalleryService
from app.api.v1.board.post.service import PostService
from app.api.v1.user.account.service import AccountService
from app.api.v1.board.comment.service import CommentService


class Report(Resource):
    @GalleryService.gallery_manager_required
    def get(self, gallery_id, report_id):
        return self.dump_report(ReportService.get_report_by_id(report_id))

    def dump_report(self, report):
        content_type = report.reported_content_type

        if content_type == ContentType.COMMENT.value:
            return comment_report_schema.dump(report)
        elif content_type == ContentType.POST.value:
            return post_report_schema.dump(report)
        else:
            abort(500)

    @GalleryService.gallery_manager_required
    def delete(self, gallery_id, report_id):
        return ReportService.delete_report(report_id)


class ReportList(Resource):
    @GalleryService.gallery_manager_required
    def get(self, gallery_id):
        reports = reports_schema.dump(ReportListService.get_reports_by_gallery_id(gallery_id))

        return reports, 200

    @jwt_required
    def post(self, gallery_id):
        request_account = AccountService.find_account_by_email(get_jwt_identity())
        create_report_data = self.validate_json_body(request.json)

        self.check_reported_write_is_exist(create_report_data)
        GalleryService.get_gallery_by_id(gallery_id)

        ReportListService.create_new_report(
            reporter=request_account.user,
            reported_content_type=create_report_data['reported_content_type'],
            reason=create_report_data['reason'],
            detail_reason=create_report_data['detail_reason'],
            comment_id=create_report_data.get('comment_id'),
            post_id=create_report_data.get('post_id'),
            gallery_id=gallery_id
        )

        return {}, 201

    def validate_json_body(self, json):
        RequestValidator.validate_request(ReportInputSchema(), json)

        content_type = json['reported_content_type']
        if content_type == ContentType.POST.value:
            validate_schema = ReportPostInputSchema()
        elif content_type == ContentType.COMMENT.value:
            validate_schema = ReportCommentInputSchema()

        RequestValidator.validate_request(validate_schema, json)

        if json.get('comment_id') and json.get('post_id'):
            abort(400, 'comment id and post id can be together')

        return json

    def check_reported_write_is_exist(self, json):
        if json['reported_content_type'] == ContentType.POST.value:
            PostService.abort_if_not_exist_post_id(json['post_id'])
        elif json['reported_content_type'] == ContentType.COMMENT.value:
            CommentService.abort_if_not_exist_comment_id(json['comment_id'])