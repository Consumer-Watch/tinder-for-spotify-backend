from models.user import User
from flask import request, jsonify
from config.database import db
from models.usertopartists import UserTopArtists
from models.usertoptracks import UserTopTracks
from utils.responses import success_response, error_response
import requests

from validators.spotify import SpotifyError


def create_user(user_data: any):
    try:
        user = User.query.get(user_data["id"])
        
        if user is not None:
            user = user.toDict()
            return success_response(user)
        
        new_user = User(
            id = user_data["id"],
            spotify_username = user_data["display_name"],
            name = user_data["display_name"],
            bio = "",
            email = user_data["email"],
            profile_image = user_data["images"][-1]["url"],
            country = user_data["country"],
            banner = "",
            friend_count = 0
        )
        db.session.add(new_user)
        db.session.commit()
        return success_response(user_data, 201)
    
    except SpotifyError as error:
        return error_response(error.status_code, error.message)

    except Exception as e:
        return error_response(500, str(e))



def get_user(id: str):
    user = User.query.get(id).toDict()
    if user is None:
        return error_response(404, "User does not exist")
    
    return success_response(user)

def update_user(id: str, updated_fields: any):

    try:
        user = User.query.get(id)

        if user is None:
            return error_response(404, "User does not exist")
        
        User.query.filter_by(id = id).update(values={**updated_fields})
        db.session.commit()
        return success_response(None, 200)
    except Exception as e:
        return error_response(500, str(e))
    

def get_all_users():
    try:
        
        users = db.session.query(User, UserTopArtists, UserTopTracks).join(
            UserTopArtists
        ).all()


        users = [{
            **user.toDict(),
            "artist": user_top_artists.toDict()["artists"]["data"][0],
            "track": user_top_tracks.toDict()["tracks"]["data"][0],

        } for (
            user, 
            user_top_artists, 
            user_top_tracks
        ) in users]

        return success_response(users)
    except Exception as e:
        return error_response(500, str(e))
    
