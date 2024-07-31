from datetime import datetime
from models.usertopgenres import UserTopGenres
from config.database import db
from services.spotify import SpotifyService
from utils.functions import generate_random_id, get_future_date

def create_top_genres(user_id: str, authorization: str):
    existing_top_genres = UserTopGenres.query.filter_by(user_id = user_id).one_or_none()
    

    if existing_top_genres is None:
        top_items = SpotifyService.get_top_items_genres(authorization)

        genres = { "data" : top_items }

        new_id = generate_random_id(15)
        new_top_genres = UserTopGenres(
            id = new_id,
            user_id = user_id,
            genres = genres,
        )
        db.session.add(new_top_genres)
        db.session.commit()
        return new_top_genres.toDict()["genres"]
    
    top_genres = existing_top_genres.toDict()
    if top_genres["next_update"] < datetime.now():
        top_items = SpotifyService.get_top_items_genres(authorization)
        genres = { "data" : top_items }

        updated_date = get_future_date(top_genres['next_update'])
        UserTopGenres.query.filter_by(id = top_genres["id"]).update(
            values={
                "genres": genres,
                "next_update": updated_date
            }
        )
        db.session.commit()
        #return updated genres if top genres are updated
        return genres

    return top_genres["genres"]

def get_top_genres(id: str):

    top_genres = UserTopGenres.query.filter_by(user_id = id).one_or_none()    
    if top_genres is None:
        return { "data": [] }
    
    return top_genres.toDict()["genres"]

    
    
def delete_top_genres(user_id: str):
    UserTopGenres.query.filter_by(
        user_id = user_id
    ).delete()


    db.session.commit()
