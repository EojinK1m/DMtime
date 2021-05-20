from flask import abort
from app.extentions import db


class DBHelper:
    @staticmethod
    def add_model(model):
        try:
            db.session.add(model)
            db.session.flush()
        except Exception:
            abort(500, "Error occur while processing request.")
