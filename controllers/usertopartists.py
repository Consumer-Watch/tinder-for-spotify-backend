from models.usertopartists import UserTopArtists
from config.database import db
from services.spotify import SpotifyService
from utils.functions import generate_random_id
from utils.spotify import get_top_items_from_api as top_artists

def create_top_artist(user_id: str, authorization: str):
    existing_top_artist = UserTopArtists.query.filter_by(user_id = user_id).one_or_none()
    

    if existing_top_artist is None:
        top_items = SpotifyService.get_top_items(authorization, "artists")

        artists = { "data" : top_items }

        new_id = generate_random_id(15)
        new_top_artist = UserTopArtists(
            id = new_id,
            user_id = user_id,
            artists = artists,
        )
        db.session.add(new_top_artist)
        db.session.commit()
        return new_top_artist.toDict()["artists"]
    
    return existing_top_artist.toDict()["artists"]


def get_top_artists(id: str):

    top_artists = UserTopArtists.query.filter_by(user_id = id).one_or_none()    
    if top_artists is None:
        return { "data": [] }
    
    return top_artists.toDict()["artists"]
    


def delete_top_artists(user_id: str):
    UserTopArtists.query.filter_by(
        user_id = user_id
    ).delete()

    db.session.commit()




    