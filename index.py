from flask import Flask, request, redirect, jsonify
from spotify_config import spotify
import requests
import os
from utils.responses import success_response, error_response

app = Flask(__name__)

file_write = open("tokens.txt", "a")

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
        "scope": "user-read-private user-read-email user-top-read user-library-read user-read-currently-playing",
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
    try:
        data = spotify(code)
        return success_response(data) #client should store this
    except:
        return error_response()


@app.route('/me')
def me_route():
    request_body = request.get_json()
    access_token = request_body.get('access_token', None)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        data = requests.get("https://api.spotify.com/v1/me", headers=headers)
        #data2 = requests.get("https://api.spotify.com/v1/me/top/artists", headers=headers)
        profile_data = data.json()
        return success_response(profile_data)
    except:
        return error_response()

if __name__ == "__main__":
    app.run(debug=True)