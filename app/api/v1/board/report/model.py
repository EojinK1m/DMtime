from app.extentions import db


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
    comment_id = db.Column(
        db.Integer(),
        db.ForeignKey("comment.id", ondelete="SET NULL"),
        nullable=True,
    )

    @property
    def nested_gallery(self):
        return self.reported_comment.wrote_post.posted_gallery

    def add(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)



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
    post_id = db.Column(
        db.Integer(),
        db.ForeignKey("post.id", ondelete="SET NULL"),
        nullable=True,
    )

    @property
    def nested_gallery(self):
        return self.reported_post.posted_gallery

    def add(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)