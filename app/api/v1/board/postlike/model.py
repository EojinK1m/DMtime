
from app import db

class PostLikeModel(db.Model):
    __tablename__ = "postlike"

    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(
        db.Integer(),
        db.ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
    )
    liker_id = db.Column(
        db.String(320),
        db.ForeignKey("user.email", ondelete="CASCADE"),
        nullable=False
    )
    
class PostDislikeModel(db.Model):
    __tablename__ = "postdislike"

    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(
        db.Integer(),
        db.ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
    )
    liker_id = db.Column(
        db.String(320),
        db.ForeignKey("user.email", ondelete="CASCADE"),
        nullable=False,
    )