from datetime import datetime
from models.usertopartists import UserTopArtists
from config.database import db
from services.spotify import SpotifyService
from utils.functions import generate_random_id, get_future_date

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
    
    top_artist = existing_top_artist.toDict()
    if top_artist['next_update'] is None or top_artist["next_update"] < datetime.now():
        top_items = SpotifyService.get_top_items(authorization, "artists")
        artists = { "data" : top_items }

        updated_date = get_future_date(top_artist['next_update'])
        UserTopArtists.query.filter_by(id = existing_top_artist.toDict()["id"]).update(
            values={
                "artists": artists,
                "next_update": updated_date
            }
        )
        db.session.commit()
        #return updated Artists if top artists are updated
        
        return artists

    

    return top_artist["artists"]


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




    