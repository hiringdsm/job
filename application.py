from flask import Flask

upload_folder = 'uploads/'

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['SECURITY_REGISTERABLE'] = True
