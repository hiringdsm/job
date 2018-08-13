from datetime import datetime
from database import db


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)
    company = db.Column(db.String(100))
    image = db.Column(db.String)
    role = db.Column(db.String(100))
    featured = db.Column(db.Boolean(False))
    link = db.Column(db.String)
    location_id = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, company, role, featured, link, image, location_id):
        self.user_id = user_id
        self.company = company
        self.role = role
        self.featured = featured
        self.link = link
        self.image = image
        self.location_id = location_id

    def __repr__(self):
        return '<models.Job[company=%s;role=%s]>' % (self.company, self.role)
