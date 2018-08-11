from database import db
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

from models.user import User
from models.role import Role
from models.job import Job
from models.location import Location

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
