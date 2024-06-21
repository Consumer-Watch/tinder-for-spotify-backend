from config.app import app
from flask import request
from controllers.user import get_all_users, get_user
from controllers.usertopartists import get_top_artists
from services.spotify import SpotifyService
from utils.responses import error_response, success_response
from utils.spotify import get_top_items_from_api

from controllers.usertopartists import create_top_artist
from controllers.usertoptracks import create_top_track, get_top_tracks
from validators.spotify import SpotifyError

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
    if request.method != "POST":
        return error_response(405, "Method not allowed")
    
    authorization = request.headers.get('Authorization', None)

    if authorization is None or authorization == '':
        return error_response(400, "Authorization Header not present")

    user_id = request.get_json().get('user_id', None);
    try:
        if type == "artists":
            top_items = create_top_artist(user_id, authorization)
            
        elif type == "tracks":
            top_items = create_top_track(user_id, authorization)
            
        else:
            return error_response(400, "Invalid Selection")

        return success_response(top_items["data"], 201)
    
    except SpotifyError as error:
        return error_response(error.status_code, error.message)

    except Exception as e:
        return error_response(500, str(e))
    
@app.route('/users/me/playing', methods=['GET'])
def currently_playing():
    country = request.args.get('country', None)
    authorization = request.headers['Authorization']

    if country == '' or country is None:
        return error_response(400, 'country is not present in params')
    
    if authorization is None or authorization == '':
        return error_response(401, 'Authorization Header not present')

    try:
        current_playing_data = SpotifyService.currently_playing_track(authorization, country)
        return success_response(current_playing_data, 200)
    except SpotifyError as error:
        return error_response(error.status_code, error.message)
    except Exception as error:
        return error_response(500, str(error))


@app.route('/users')
def get_similar_users():
    return get_all_users()