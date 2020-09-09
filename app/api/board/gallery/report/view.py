from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.api.board.gallery.report.service import ReportService, ReportListService
from app.api.board.gallery.service import GalleryService

class Report(Resource):
    @GalleryService.gallery_manager_required
    def get(self, gallery_id, report_id):
        return make_response(ReportService.provide_report(gallery_id=gallery_id, report_id=report_id))

    @GalleryService.gallery_manager_required
    def delete(self, gallery_id, report_id):
        return make_response(ReportService.delete_report(gallery_id=gallery_id, report_id=report_id))


class ReportList(Resource):
    @GalleryService.gallery_manager_required
    def get(self, gallery_id):
        return make_response(ReportListService.provide_report_list(gallery_id=gallery_id))

    @jwt_required
    def post(self, gallery_id):
        return make_response(ReportListService.create_report(gallery_id=gallery_id, json=request.json))
