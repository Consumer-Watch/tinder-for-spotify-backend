from flask import Flask, request, redirect, jsonify
from services.spotify import SpotifyService
from spotify_config import spotify
import requests
import os
from utils.responses import success_response, error_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config.app import app
from config.database import db

from controllers.user import create_user
from routes import user, friends
from models.usertopgenres import UserTopGenres
from validators.spotify import SpotifyError


migrate = Migrate(app, db)
#db.init_app(app)
migrate.init_app(app, db)
#manager = Manager(app)

#manager.add_command('db', migrate)


@app.route("/")
def welcome():
    return "Welcome to Spotinder!"

@app.route('/login', methods=["GET"])
def index_route():

    url = "https://accounts.spotify.com/authorize" 
     # replace with your actual API endpoint
    body = { 
        "client_id": os.getenv("CLIENT_ID"),   
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "scope": "user-read-private user-read-email user-top-read user-library-read user-read-currently-playing user-read-playback-state",
        "response_type": "code"
    }  # replace with your actual request body
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "grant_type": "refresh_token"
    }
    try:
        data = requests.get(url, params=body, headers=headers)
        response_data = { "url": data.url }
        return success_response(response_data)
    except:
        return error_response()


@app.route('/token')
def profile():
    code = request.args.get("code")
    if code == None:
        return error_response(400, "No Authorization Code In Params")
    
    try:
        data = SpotifyService.get_credentials(code)
        return success_response(data) #client should store this
    except:
        return error_response()
    
@app.route('/renew-token')
def renew_token():
    refresh_token = request.headers['Refresh']

    if refresh_token == None:
        return error_response(400, "No refresh token in request")    

    try:
        reponse_data = SpotifyService.renew_token(refresh_token);
        return success_response(reponse_data)
    except Exception as e:
        return error_response(500, str(e))


@app.route('/me')
def me_route():
    authorization = request.headers['Authorization']

    if authorization == None:
        return error_response(400, "Access Token not present in request")

    try:
        profile_data = SpotifyService.get_current_user(authorization)
        #id_cache.set(access_token, profile_data["id"])
        return create_user(profile_data)
    
    except SpotifyError as error:
        return error_response(error.status_code, error.message)
    
    except Exception as e:
        return error_response(500, str(e))
    
    
environment = os.getenv("ENV")
debug_mode = False if environment == 'prod' else True

if __name__ == "__main__":
    app.run(debug=debug_mode)
