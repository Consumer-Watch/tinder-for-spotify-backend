from datetime import datetime
from models.usertoptracks import UserTopTracks
from services.spotify import SpotifyService
from utils.functions import generate_random_id, get_future_date
from config.database import db
from utils.spotify import get_top_items_from_api as top_tracks


def create_top_track(user_id: str, authorization: str):
    existing_top_track = UserTopTracks.query.filter_by(
        user_id = user_id,
    ).one_or_none()

    if existing_top_track is None:
        top_items = SpotifyService.get_top_items(authorization, "tracks")

        tracks = { "data" : top_items }

        new_id = generate_random_id(15)
        new_top_track = UserTopTracks(
            id = new_id,
            user_id = user_id,  
            tracks = tracks
        )

        db.session.add(new_top_track)
        db.session.commit()
        return new_top_track.toDict()["tracks"]
    
    top_tracks = existing_top_track.toDict()

    if top_tracks["next_update"] < datetime.now:
        top_items = SpotifyService.get_top_items(authorization, "artists")
        tracks = { "data" : top_items }

        updated_date = get_future_date(top_tracks['next_update'])
        UserTopTracks.query.filter_by(id = existing_top_track.toDict()["id"]).update(
            tracks = tracks,
            next_update = updated_date
        )
        db.session.commit()

    
    return top_tracks["tracks"]
    

def delete_top_tracks(user_id: str):
    UserTopTracks.query.filter_by(user_id = user_id).delete()
    db.session.commit()

def get_top_tracks(user_id: str):
    top_tracks = UserTopTracks.query.filter_by(user_id = user_id).one_or_none()

    if top_tracks is None:
        return { "data": [] }

    return top_tracks.toDict()["tracks"]    
