from config.database import db
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timedelta

from utils.functions import get_future_date

DEFAULT_UPDATE_INTERVAL_DAYS = 30

class UserTopGenres(db.Model):
    __tablename__ = "users-top-genres"

    id = db.Column(db.String(15), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), index=True)
    #artist_id = db.Column(db.String(), db.ForeignKey('artists.id'), index=True)
    #position_for_user = db.Column(db.Integer)
    genres = db.Column(JSONB)
    next_update = db.Column(db.DateTime, default= lambda : get_future_date(datetime.today(), DEFAULT_UPDATE_INTERVAL_DAYS))

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
