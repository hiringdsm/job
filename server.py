from flask import render_template, request, redirect
from flask_security import Security, logout_user, login_required
from flask_security.utils import encrypt_password, verify_password
from flask_restless import APIManager
from flask_jwt import JWT, jwt_required

from database import db
from application import app
from models import User, user_datastore, Role, Job, Location
from admin import init_admin
from resources import job

# Setup Flask-Security  =======================================================
security = Security(app, user_datastore)

@app.route('/logout')
def log_out():
    logout_user()
    return {"status": 200}

# Job Routes
@app.route('/job/<id>', methods=['GET'])
@jwt_required()
def job_get(id):
    return job.get(id)

@app.route('/job', methods=['POST'])
@jwt_required()
def job_post():
    data = request.get_json(silent=True)
    return job.post(data)


# JWT Token authentication  ===================================================
def authenticate(username, password):
    user = user_datastore.find_user(email=username)
    if user and username == user.email and verify_password(password, user.password):
        return user
    return None


def load_user(payload):
    user = user_datastore.find_user(id=payload['identity'])
    return user


jwt = JWT(app, authenticate, load_user)

# Flask-Restless API  =========================================================
@jwt_required()
def auth_func(**kw):
    pass


apimanager = APIManager(app, flask_sqlalchemy_db=db)


# Setup Admin  ================================================================
init_admin()


# Bootstrap  ==================================================================
def create_test_models():
    user_datastore.create_user(email='test', password=encrypt_password('test'))
    user_datastore.create_user(email='test2', password=encrypt_password('test2'))
    db.session.commit()


@app.before_first_request
def bootstrap_app():
    if not app.config['TESTING']:
        if db.session.query(User).count() == 0:
            create_test_models()


# Start server  ===============================================================
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
