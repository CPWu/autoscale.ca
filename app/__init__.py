from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config)
# Initialize DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
app.app_context().push()
db.create_all()