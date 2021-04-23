from app import db


class CommentReport(db.Model):
    __tablename__ = "comment_report"

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Integer(), nullable=False)
    detail_reason = db.Column(db.String(500), nullable=False)
    user_id = db.Column(
        db.String(320),
        db.ForeignKey("user.email", ondelete="CASCADE"),
        nullable=False,
    )
    gallery_id = db.Column(
        db.String(30),
        db.ForeignKey("gallery.gallery_id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id = db.Column(
        db.Integer(),
        db.ForeignKey("post.id", ondelete="SET NULL"),
        nullable=True,
    )
    comment_id = db.Column(
        db.Integer(),
        db.ForeignKey("comment.id", ondelete="SET NULL"),
        nullable=True,
    )

    reporter = db.relationship("UserModel")
    reported_comment = db.relationship("PostModel")

    def add(self):
        db.session.add(self)


class PostReport(db.Model):
    __tablename__ = "post_report"

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Integer(), nullable=False)
    detail_reason = db.Column(db.String(500), nullable=False)
    user_id = db.Column(
        db.String(320),
        db.ForeignKey("user.email", ondelete="CASCADE"),
        nullable=False,
    )
    gallery_id = db.Column(
        db.String(30),
        db.ForeignKey("gallery.gallery_id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id = db.Column(
        db.Integer(),
        db.ForeignKey("post.id", ondelete="SET NULL"),
        nullable=True,
    )

    reporter = db.relationship("UserModel")
    reported_post = db.relationship("PostModel")

    def add(self):
        db.session.add(self)
