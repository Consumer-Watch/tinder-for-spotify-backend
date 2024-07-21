from models.friends import FriendRequests
from models.user import User
from config.database import db
from models.usertopartists import UserTopArtists
from models.usertoptracks import UserTopTracks
from models.usertopgenres import UserTopGenres
from utils.responses import success_response, error_response
from datetime import datetime
from validators.spotify import SpotifyError


def get_or_create_user(user_data: any):
    user_instance = User.query.get(user_data["id"])
    if user_instance is not None:
        user = user_instance.toDict()
        return success_response(user, 200)
    
    new_user = User(
        id = user_data["id"],
        spotify_username = user_data["display_name"],
        name = user_data["display_name"],
        bio = "",
        email = user_data["email"],
        profile_image = user_data["images"][-1]["url"] if user_data["images"] else "",
        country = user_data["country"],
        banner = "https://firebasestorage.googleapis.com/v0/b/sonder-63ac2.appspot.com/o/banners%2Fdefault-banner%20(1).png?alt=media&token=950a6bec-fb22-4df2-b6e7-553fc861658c",
        friend_count = 0
    )
    db.session.add(new_user)
    db.session.commit()

    new_user = new_user.toDict()
    return success_response(new_user, 201)
   

def get_user(id: str):
    user = User.query.get(id)
    
    if user is None:
        return error_response(404, "User does not exist")
    
    user_dict = user.toDict()
    
    user = {
        **user_dict,
        "created_at": user_dict["created_at"].strftime("%B %Y") if user_dict.get("created_at") else None
    }
    
    return success_response(user)

def update_user(id: str, updated_fields: any):

    try:
        user = User.query.get(id)

        if user is None:
            return error_response(404, "User does not exist")
                
        User.query.filter_by(id = id).update(values=updated_fields)
        db.session.commit()
        return success_response(None, 200)
    except Exception as e:
        return error_response(500, str(e))
    

def get_all_users(user_id: str):
    try:
        
        users = db.session.query(User, UserTopArtists, UserTopTracks, UserTopGenres).\
        join(UserTopArtists).\
        join(UserTopTracks).\
        join(UserTopGenres).\
        join(FriendRequests, FriendRequests.user_id != User.id).\
        filter(User.id != user_id).\
        filter(FriendRequests.user_id != user_id).\
        filter(FriendRequests.friend_id != user_id).\
        all()
        
        users = [{
            **user.toDict(),
            "artist": user_top_artists.toDict()["artists"]["data"][0],
            "track": user_top_tracks.toDict()["tracks"]["data"][0],
            "likes": user_top_genres.toDict()["genres"]["data"]

        } for (
            user, 
            user_top_artists, 
            user_top_tracks,
            user_top_genres
        ) in users]

        return success_response(users)
    except Exception as e:
        return error_response(500, str(e))
    
