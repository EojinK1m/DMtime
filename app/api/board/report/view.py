from flask import make_response
from flask_restful import Resource

from app.api.board.report.service import PostReportService

class PostReport(Resource):
    def get(self):
        return make_response()
    
class PostReportList(Resource):
    def get(self):
        return make_response()
    