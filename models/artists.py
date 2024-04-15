from config.database import db
from sqlalchemy import inspect
from datetime import datetime


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(60))
    image = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
