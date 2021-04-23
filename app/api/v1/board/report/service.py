from flask import abort

from .model import PostReport, CommentReport


class CommentReportService:
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
        if not (report.gallery_id == int(gallery_id)):
            raise Exception(f"{report.gallery_id}, {gallery_id}")


class CommentReportListService:
    @staticmethod
    def create_new_report(
        gallery_id,
        reported_content_type,
        comment_id,
        post_id,
        reason,
        detail_reason,
        reporter,
    ):
        try:
            new_report = ReportModel(
                reported_content_type=reported_content_type,
                comment_id=comment_id,
                post_id=post_id,
                reason=reason,
                detail_reason=detail_reason,
                gallery_id=gallery_id,
                reporter=reporter,
            )
            new_report.add_report()
            db.session.commit()

            return new_report
        except:
            abort(500, "An error occurred in server")

    @staticmethod
    def provide_report_list(gallery_id):
        reports = ReportListService.get_reports_by_gallery_id(gallery_id)
        return (
            jsonify(
                msg="query_succceed", reports=reports_schema.dumps(reports)
            ),
            200,
        )

    @staticmethod
    def get_reports_by_gallery_id(gallery_id):
        try:
            return ReportModel.query.filter_by(gallery_id=gallery_id)
        except:
            abort(500, "An error occurred ")


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
