from config.app import app
from flask import request
from controllers.user import get_user
from controllers.usertopartists import get_top_artists
from utils.responses import success_response
from utils.spotify import get_top_items_from_api

from controllers.artists import create_artist
from controllers.usertopartists import create_top_artist
from config.redis import id_cache
import asyncio

@app.route('/users/<id>', methods=["GET", "PUT", "DELETE"])
def users_route(id: str):
    if request.method == "GET":
        return get_user(id)
    
@app.route('/users/<id>/top/<type>')
def user_top_items(id: str, type: str):
    if type == 'artists':
        return get_top_artists(id)
    else:
        pass

    
@app.route('/users/me/top/<type>', methods=["POST", "GET"])
def get_top_items(type: str):
    access_token = request.get_json().get('access_token', None);
    user_id = request.get_json().get('user_id', None);

    print("user_id", user_id)
    top_items = get_top_items_from_api(
        type = type,
        access_token = access_token
    )
    
    if type == "artists":
        for artist in top_items:
            create_artist(artist)
            create_top_artist(user_id=user_id, artist_id=artist["id"], position=artist["position"])
        return success_response(top_items)

    else:
        pass