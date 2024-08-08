from datetime import datetime
from models.user import User
from models.usertopgenres import UserTopGenres
from config.database import db
from services.spotify import SpotifyService
from utils.embeddings import create_embeddings
from utils.functions import generate_random_id, get_future_date
from serializers.user import user_schema
from controllers.user import update_user
from utils.pinecone import push_vectors



def create_top_genres(user_id: str, authorization: str):
    existing_top_genres = UserTopGenres.query.filter_by(user_id = user_id).one_or_none()
    

    if existing_top_genres is None:
        top_items, top_artists = SpotifyService.get_top_items_genres(authorization)

        genres = { "data" : top_items }

        new_id = generate_random_id(7)
        new_top_genres = UserTopGenres(
            id = new_id,
            user_id = user_id,
            genres = genres,
        )
        db.session.add(new_top_genres)
        db.session.commit()

        user = User.query.get({"id" : user_id})
        user = user_schema.dump(user)
        artists = [artist["name"] for artist in top_artists]
        likes = top_items

        text = ", ".join(top_items) + " " + ", ".join()

        user_metadata = {
            "bio": user['bio'],
            "artists": artists,
            "likes": likes,
            "id": user['id'],
            "name": user['name'],
            "spotify_username": user['spotify_username'],
            "profile_image": user['profile_image'],
        }
        embedding = create_embeddings(text)
        update_user(user['id'], { "data_embedding": embedding })
        push_vectors(embedding=create_embeddings(text), metadata=user_metadata)
        
        return new_top_genres.toDict()["genres"]
    
    top_genres = existing_top_genres.toDict()

    if top_genres["next_update"] < datetime.now():
        top_items, top_artists = SpotifyService.get_top_items_genres(authorization)
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

        user = User.query.get({"id" : user_id})
        user = user_schema.dump(user)
        artists = [artist["name"] for artist in top_artists]
        likes = top_items

        text = ", ".join(top_items) + " " + ", ".join(artists)

        user_metadata = {
            "bio": user['bio'],
            "artists": artists,
            "likes": likes,
            "id": user['id'],
            "name": user['name'],
            "spotify_username": user['spotify_username'],
            "profile_image": user['profile_image'],
        }
        embedding = create_embeddings(text)
        update_user(user['id'], { "data_embedding": embedding })
        push_vectors(embedding=create_embeddings(text), metadata=user_metadata)

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
