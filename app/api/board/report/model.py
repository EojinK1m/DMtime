from app import db, ma


class PostReport(db.Model):
    __tablename__ = 'post_report'

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(), nullalble=False)
    posted_user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullalble=False)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullalble=False)
