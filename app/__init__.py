from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor

app = Flask(__name__)
# Adds CKEditor
ckeditor = CKEditor(app)

app.config.from_object(Config)
# Initialize DB
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from app import routes, models
app.app_context().push()
db.create_all()