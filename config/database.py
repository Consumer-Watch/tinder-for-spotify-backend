import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from config.app import app

DATABASE_URL = {
    "prod": os.getenv("DATABASE_PROD_URL"),
    "dev": os.getenv("DATABASE_URL")
}


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL[os.getenv("ENV")]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

#db.session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
migrate = Migrate(app, db)