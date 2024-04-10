from config.database import db

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50))
    spotify_username = db.Column(db.String(64), index=True, unique=True)
    bio = db.Column(db.String(120))