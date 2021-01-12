from werkzeug import exceptions
from flask import jsonify, abort
from flask_jwt_extended import get_jwt_identity

from app import db
from app.api.v1.board.gallery.report.model import\
    ReportModel,\
    reports_schema,\
    comment_report_schema,\
    post_report_schema,\
    ReportInputSchema,\
    ReportCommentInputSchema,\
    ReportPostInputSchema,\
    ContentType
from app.api.v1.user.model import UserModel
from app.api.v1.board.gallery.service import GalleryService
from app.api.v1.board.comment.service import CommentService
from app.api.v1.board.post.service import PostService



class ReportService:

    @staticmethod
    def delete_report(report_id):
        target_report = ReportService.get_report_by_id(report_id)

        try:
            target_report.delete_report()
        except:
            abort(500)

    @staticmethod
    def get_report_by_id(report_id):
        report = ReportModel.query.get(report_id)
        
        if report is None:
            abort(404)

        return report

    @staticmethod
    def raise_if_not_report_of_gallery(report, gallery_id):
        if not(report.gallery_id == int(gallery_id)):
            raise Exception(f'{report.gallery_id}, {gallery_id}')



class ReportListService:

    @staticmethod
    def create_new_report(
            gallery_id,
            reported_content_type,
            comment_id,
            post_id,
            reason,
            detail_reason,
            reporter
    ):
        try:
            new_report = ReportModel(
                reported_content_type=reported_content_type,
                comment_id=comment_id,
                post_id=post_id,
                reason=reason,
                detail_reason=detail_reason,
                gallery_id=gallery_id,
                reporter=reporter
            )
            new_report.add_report()
            db.session.commit()

            return new_report
        except:
            abort(500, 'An error occurred in server')

    @staticmethod
    def provide_report_list(gallery_id):
        reports = ReportListService.get_reports_by_gallery_id(gallery_id)
        return\
            jsonify(
                msg='query_succceed',
                reports=reports_schema.dumps(reports)
            ), 200

    @staticmethod
    def get_reports_by_gallery_id(gallery_id):
        try:
            return ReportModel.query.filter_by(gallery_id=gallery_id)
        except:
            abort(500, 'An error occurred ')


def validate_json_body(json):
    errors = ReportInputSchema().validate(json)
    if (errors):
        abort(400, str(errors))

    content_type = json.get('reported_content_type')
    if(content_type == ContentType.POST.value):
        validate_schema = ReportPostInputSchema()
    elif(content_type == ContentType.COMMENT.value):
        validate_schema = ReportCommentInputSchema()

    error = validate_schema.validate(json)
    if (error):
        abort(400, str(error))

    if(json.get('comment_id') and json.get('post_id')):
        abort(400, 'comment id and post id can be together')


def check_reported_write_is_exist(json):
    if (json['reported_content_type'] == ContentType.POST.value):
        PostService.abort_if_not_exist_post_id(json['post_id'])
    elif (json['reported_content_type'] == ContentType.COMMENT.value):
        CommentService.abort_if_not_exist_comment_id(json['comment_id'])


