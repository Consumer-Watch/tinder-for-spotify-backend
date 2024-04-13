from config.database import db
from sqlalchemy import inspect
from datetime import datetime

class UserTopArtists(db.Model):
    __tablename__ = "users-top-artists"

    id = db.Column(db.String(15), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), index=True)
    artist_id = db.Column(db.String(), db.ForeignKey('artists.id'), index=True)
    position_for_user = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
