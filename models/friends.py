from config.database import db
from sqlalchemy import inspect
from datetime import datetime
from enum import Enum

class FriendRequestStatus(Enum):
    pending = "pending"
    accepted = "accepted"
    rejeted = "rejected"
    blocked = "blocked"

class FriendRequests(db.Model):
    __tablename__ = "friend-requests"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), index=True)
    sender_username = db.Column(db.String(50))
    sender_avatar = db.Column(db.String)
    friend_id = db.Column(db.String(50), db.ForeignKey('users.id'), index=True)
    status = db.Column(db.Enum(FriendRequestStatus))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

