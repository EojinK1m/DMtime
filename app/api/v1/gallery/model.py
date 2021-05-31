from app.extensions import db

GALLERY_TYPES = {"special": 0, "default": 1, "user": 2}


class GalleryModel(db.Model):
    __tablename__ = "gallery"

    gallery_id = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.String(255), nullable=True)
    manager_user_id = db.Column(
        db.String(320),
        db.ForeignKey(
            "user.email",
            ondelete="CASCADE"
        )
    )
    gallery_type = db.Column(db.Integer(), nullable=False)

    posts = db.relationship(
        "PostModel", passive_deletes=True, backref="posted_gallery"
    )

    def delete_gallery(self):
        db.session.delete(self)

    def is_manager(self, user):
        return user.email == self.manager_user_id

    def patch(self, name, explain):
        self.name = name if name is not None else self.name
        self.explain = explain if explain is not None else self.explain

        db.session.commit()

    @property
    def id(self):
        return self.gallery_id


