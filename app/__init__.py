from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key =
app.config.from_object('config')
db = SQLAlchemy(app)

from app import models, controllers

app.register_blueprint(controllers.index)
app.register_blueprint(controllers.teams)
app.register_blueprint(controllers.tasks)
app.register_blueprint(controllers.login_api)
