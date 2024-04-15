from models.artists import Artist
from config.database import db

def create_artist(artist_data: any):
    existing_artist = Artist.query.get(artist_data["id"])

    if existing_artist is None:
        new_artist = Artist(
            name = artist_data["name"],
            id = artist_data["id"],
            image = artist_data["image"],
        )
        db.session.add(new_artist)
        db.session.commit()
    
    return artist_data["id"]

def delete_artist(id: str):
    deleted_artist = Artist.query.get(id)
    db.session.delete(deleted_artist)
    db.session.commit()
