import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.app import app



app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)