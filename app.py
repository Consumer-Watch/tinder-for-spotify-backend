from flask import Flask, request, redirect, jsonify
from flask_mail import Message
from services.spotify import SpotifyService
import requests
import os
from utils.functions import send_email_to_user
from utils.responses import success_response, error_response
from flask_migrate import Migrate

from config.app import app
from config.database import db
from config.mail import mail


from routes import user, friends


migrate = Migrate(app, db)
#db.init_app(app)
migrate.init_app(app, db)
#manager = Manager(app)

#manager.add_command('db', migrate)






@app.route("/")
def welcome():
    #Firebase.add_to_firestore({ "hello": "day" })
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

@app.route('/mail', methods=["GET"])
def send_mail():
    send_email_to_user("hello", "testing", ["fortune0208@yahoo.com"])
    return 'Email sent succesfully!'

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
    
    
environment = os.getenv("ENV")
debug_mode = False if environment == 'prod' else True

if __name__ == "__main__":
    app.run(debug=debug_mode)
