from app.extentions import db


class PostlikeModel(db.Model):
    __tablename__ = "postlike"

    post_id = db.Column(
        db.Integer(),
        db.ForeignKey("post.id", ondelete="CASCADE"),
        primary_key=True,
    )
    liker_id = db.Column(
        db.String(320),
        db.ForeignKey("user.email", ondelete="CASCADE"),
        primary_key=True
    )

    def delete(self):
        db.session.delete(self)
    # included_post = db.relationship(
    #     'PostModel',
    #     back_populates='dislikes'
    # )
    # included_post = db.relationship('PostModel', back_populates="likes")


class PostdislikeModel(db.Model):
    __tablename__ = "postdislike"

    post_id = db.Column(
        db.Integer(),
        db.ForeignKey("post.id", ondelete="CASCADE"),
        primary_key=True
    )
    liker_id = db.Column(
        db.String(320),
        db.ForeignKey("user.email", ondelete="CASCADE"),
        primary_key=True
    )

    def delete(self):
        db.session.delete(self)

    # included_post = db.relationship(
    #     'PostModel',
    #     back_populates='dislikes'
    # )
    # backref=db.backref('teams_membership', cascade='delete, delete-orphan')
