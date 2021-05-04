from flask import abort

from app import db

from .model import PostReport, CommentReport

from ..post.model import PostModel
from ..comment.model import CommentModel
from ..gallery.model import GalleryModel

class CommentReportService:
    @classmethod
    def delete_report(cls, report_id):
        target_report = cls.get_report_by_id(report_id)

        try:
            target_report.delete_report()
        except:
            abort(500)

    @classmethod
    def get_report_by_id(cls, report_id):
        report = CommentReport.query.get(report_id)

        if report is None:
            abort(404, f'Comment report {report_id} is not found')

        return report

    @classmethod
    def raise_if_not_report_of_gallery(cls, report, gallery_id):
        if not (report.gallery_id == int(gallery_id)):
            raise Exception(f"{report.gallery_id}, {gallery_id}")


class CommentReportListService:

    @classmethod
    def get_all_comment_reports(cls):
        return CommentReport.query.all()

    @classmethod
    def create_new_report(
        cls,
        comment,
        reason,
        detail_reason,
        reporter,
    ):
        try:
            new_report = CommentReport(
                reason=reason,
                detail_reason=detail_reason,
                user_id=reporter.email,
                comment_id=comment.id
            )

            new_report.add()

            return new_report
        except:
            abort(500, "An error occurred in server")

    @classmethod
    def get_reports_by_gallery_id(cls, gallery_id):
        try:
            return CommentReport.query.filter_by(gallery_id=gallery_id)
        except:
            abort(500, "An error occurred ")

    @classmethod
    def get_comment_reports_in_gallery(cls, gallery):
        return db.session.query(CommentReport).\
            join(CommentModel).\
            join(PostModel).\
            join(GalleryModel).\
            filter_by(gallery_id=gallery.id).\
            all()


class PostReportService:
    @classmethod
    def delete_report(cls, report_id):
        target_report = cls.get_report_by_id(report_id)

        try:
            target_report.delete()
        except:
            abort(500)

    @classmethod
    def get_report_by_id(cls, report_id):
        report = PostReport.query.get(report_id)

        if report is None:
            abort(404)

        return report


class PostReportListService:
    @classmethod
    def create_new_report(
        cls,
        gallery,
        post,
        reason,
        detail_reason,
        reporter,
    ):
        try:
            new_report = PostReport(
                post_id=post.id,
                reason=reason,
                detail_reason=detail_reason,
                gallery_id=gallery.id,
                reporter=reporter,
            )
            new_report.add()

            return new_report
        except:
            abort(500, "An error occurred in server")

    @classmethod
    def get_reports_by_gallery_id(cls, gallery_id):
        try:
            return PostReport.query.filter_by(gallery_id=gallery_id)
        except:
            abort(500, "An error occurred ")
