import requests
import base64
from os import getenv

def spotify(code):

    url = "https://accounts.spotify.com/api/token" 
     # replace with your actual API endpoint
    body = { 
        "code": str(code),   
        "redirect_uri": getenv("REDIRECT_URI"),
        "grant_type": "authorization_code",
        "client_id": getenv("CLIENT_ID"),
        "client_secret": getenv("CLIENT_SECRET"),
    }  # replace with your actual request body

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = requests.post(url, data=body, headers=headers)
    return data.json()