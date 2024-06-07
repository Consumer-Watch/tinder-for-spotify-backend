from config.app import app
from flask import request
from controllers.user import get_user
from controllers.usertopartists import get_top_artists
from utils.responses import error_response, success_response
from utils.spotify import get_top_items_from_api

from controllers.usertopartists import create_top_artist
from controllers.usertoptracks import create_top_track, get_top_tracks

@app.route('/users/<id>', methods=["GET", "PUT", "DELETE"])
def users_route(id: str):
    if request.method == "GET":
        return get_user(id)
    
@app.route('/users/<id>/top/<type>')
def user_top_items(id: str, type: str):
    if type == 'artists':
        artists = get_top_artists(id)
        return success_response(artists["data"], 200)
    elif type == 'tracks':
        tracks = get_top_tracks(id)
        return success_response(tracks["data"], 200)
    else:
        return error_response(400, "Invalid Value for Type")

    
@app.route('/users/me/top/<type>', methods=["POST"])
def get_top_items(type: str):
    if request.method == "GET":
        return error_response(405, "Method not allowed")
    
    access_token = request.get_json().get('access_token', None);
    user_id = request.get_json().get('user_id', None);

    try:
        
        if type == "artists":
            top_items = create_top_artist(user_id, access_token)
            
        elif type == "tracks":
            top_items = create_top_track(user_id, access_token)
            
        else:
            return error_response(400, "Invalid Selection")

        return success_response(top_items["data"], 201)
    except Exception as e:
        return error_response(500, str(e))
