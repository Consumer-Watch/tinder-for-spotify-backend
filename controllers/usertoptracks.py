from models.usertoptracks import UserTopTracks
from services.spotify import SpotifyService
from utils.functions import generate_random_id
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
    
    return existing_top_track.toDict()["tracks"]
    

def delete_top_tracks(user_id: str):
    UserTopTracks.query.filter_by(user_id = user_id).delete()
    db.session.commit()

def get_top_tracks(user_id: str):
    top_tracks = UserTopTracks.query.filter_by(user_id = user_id).one_or_none()

    if top_tracks is None:
        return { "data": [] }

    return top_tracks.toDict()["tracks"]    
