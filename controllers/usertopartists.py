from models.usertopartists import UserTopArtists
from models.artists import Artist
from config.database import db
from utils.functions import generate_random_id
from utils.responses import success_response

def create_top_artist(user_id: str, artist_id: str, position: int):
    existing_top_artist = UserTopArtists.query.filter_by(
        artist_id = artist_id,
        user_id = user_id
    )

    if existing_top_artist is None:
        new_id = generate_random_id(15)
        new_top_artist = UserTopArtists(
            id = new_id,
            user_id = user_id,
            artist_id = artist_id,
            position_for_user = position,
        )
        db.session.add(new_top_artist)
        db.session.commit()

def get_top_artists(id: str):
    #top_artists = UserTopArtists.query.filter_by(user_id = id).order_by(UserTopArtists.position_for_user.asc())
    #top_artists = top_artists.toDict()

    top_artists = db.session.query(UserTopArtists, Artist).join(Artist, UserTopArtists.artist_id == Artist.id).filter(UserTopArtists.user_id == id).order_by(UserTopArtists.position_for_user.asc()).all()
    top_artists = [({ 
        "name": artist.toDict()["name"],
        "id": artist.toDict()["id"], 
        "image": artist.toDict()["image"],
        "position": user_top_artist.toDict()["position_for_user"] 
    }) for user_top_artist, artist in top_artists]
    return success_response(top_artists)

    


def delete_top_artists(user_id: str):
    UserTopArtists.query.filter_by(
        user_id = user_id
    ).delete()

    db.session.commit()




    