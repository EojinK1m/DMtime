from sqlalchemy.sql.functions import mode
from app.extensions import db


class BaseRepository:

    @classmethod
    def delete(cls, model):
        db.session.delete(model)
    
    @classmethod
    def add(cls, model):
        db.session.add(model)
        db.session.flush()

