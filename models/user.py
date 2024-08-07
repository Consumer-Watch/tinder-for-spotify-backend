from config.database import db
from sqlalchemy import inspect
from datetime import datetime
from pgvector.sqlalchemy import Vector


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50))
    spotify_username = db.Column(db.String(64), index=True, unique=True)
    bio = db.Column(db.String(120))
    profile_image = db.Column(db.String())
    email = db.Column(db.String(55)) #To send them email notifications
    country = db.Column(db.String(2))
    friend_count = db.Column(db.Integer, default=0)
    banner = db.Column(db.String)
    data_embedding = db.Column(Vector(768))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

