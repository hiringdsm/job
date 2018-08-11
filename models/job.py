from datetime import datetime
from database import db


class Job(db.Model):
    __tablename__ = "jobs"
    
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)
    company = db.Column(db.String(100))
    role = db.Column(db.String(100))
    featured = db.Column(db.Boolean(False))
    link = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, company, role, featured, link):
        self.user_id = user_id
        self.company = company
        self.role = role
        self.featured = featured
        self.link = link

    def __repr__(self):
        return '<models.Job[company=%s;role=%s]>' % (self.company, self.role)
