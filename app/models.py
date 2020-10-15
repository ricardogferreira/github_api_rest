from .main import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Repository(db.Model):
    name = db.Column(db.String(200), primary_key=True, autoincrement=False)
    url = db.Column(db.String(500), nullable=False, unique=True)
    access_type = db.Column(db.Boolean, default=False, nullable=False)
    size = db.Column(db.String(100), nullable=False)
    stars = db.Column(db.String(100), nullable=False)
    watchers = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("repositories", lazy=True))
    created_at = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Repository %r>" % self.name

    def __str__(self):
        return self.name or ""
