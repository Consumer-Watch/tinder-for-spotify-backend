from config.app import app
from flask import request, jsonify
from controllers.user import embed_users, get_all_users, get_or_create_user, get_user, query_for_users, update_user
from controllers.usertopartists import get_top_artists
from services.spotify import SpotifyService
from utils.gemini import ask_gemini
from utils.responses import error_response, success_response
from utils.spotify import get_top_items_from_api

from controllers.usertopgenres import create_top_genres, get_top_genres
from controllers.usertopartists import create_top_artist
from controllers.usertoptracks import create_top_track, get_top_tracks
from validators.spotify import SpotifyError

@app.route('/users/me', methods=["GET", "PUT"])
def me_route():
    authorization = request.headers['Authorization']

    if authorization == None:
        return error_response(400, "Access Token not present in request")

    try:
        profile_data = SpotifyService.get_current_user(authorization)
        user_id = profile_data.get('id')

        if request.method == "PUT":
            updated_fields = request.get_json() if request.get_json() else None
            print(updated_fields)

            if bool(updated_fields):
                return update_user(user_id, updated_fields)
                        
        else:
            return get_or_create_user(profile_data)
    
    except SpotifyError as error:
        return error_response(error.status_code, error.message)
    
    except Exception as e:
        return error_response(500, str(e))

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
    elif type == 'genres':
        genres = get_top_genres(id)
        return success_response(genres["data"], 200)
        
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

    if user_id is None or user_id == '':
        return error_response(400, "user_id is not present")
    
    try:
        if type == "artists":
            top_items = create_top_artist(user_id, authorization)
            
        elif type == "tracks":
            top_items = create_top_track(user_id, authorization)

        elif type =="genres" :
            top_items = create_top_genres(user_id,  authorization)
            
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
    
@app.route('/users/me/banner', methods=['PUT'])
def change_banner():
    user_id = request.args.get('user_id', None)
    url = request.get_json().get('url', None)

    if user_id is None or user_id == '':
        return error_response(400, "user_id is not present in query string")
    
    if url is None or url == '':
        return error_response(400, "url is not present in request body")
    
    return update_user(user_id, { "banner": url })

@app.route('/users/me/avatar', methods=['PUT'])
def change_avatar():
    user_id = request.args.get('user_id', None)
    url = request.get_json().get('url', None)

    if user_id is None or user_id == '':
        return error_response(400, "user_id is not present in query string")
    
    if url is None or url == '':
        return error_response(400, "url is not present in request body")
    
    return update_user(user_id, { "profile_image": url })


@app.route('/users')
def get_similar_users():
    user_id = request.args.get('user_id', None)
    if user_id is None or user_id == '':
        return error_response(400, "user_id is not present in query string")

    return get_all_users(user_id)

'''
@app.route('/users/vectors')
def send_users_to_vectors():
    return embed_users()


'''

@app.route('/search', methods=['POST'])
def query_users():
    query = request.args.get('query', None)

    user = request.get_json().get('user', None)

    if query is None or query == '':
        return error_response(400, "query is not present in query string")
    
    if user is None or user == '':
        return error_response(400, "user_id is not present in query string")

    user_id = user["id"]

    try:
        results = query_for_users(query, user_id)
        users = [data['metadata'] for data in results['matches']]

        summary = ask_gemini(users, user)

        answer = {
            "users": users,
            "summary": summary
        }
        return success_response(answer)
    except Exception as e:
        return error_response(500, str(e))