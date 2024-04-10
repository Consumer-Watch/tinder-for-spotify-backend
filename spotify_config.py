import requests
import base64
from os import getenv

def spotify(code):

    url = "https://accounts.spotify.com/api/token" 
     # replace with your actual API endpoint
    body = { 
        "code": str(code),   
        "redirect_uri": "http://localhost:5000/profile",
        "grant_type": "authorization_code",
        "client_id": getenv("CLIENT_ID"),
        "client_secret": getenv("CLIENT_SECRET"),
    }  # replace with your actual request body

    auth_header = base64.urlsafe_b64encode((getenv("CLIENT_ID") + ':' + getenv("CLIENT_SECRET")).encode())
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = requests.post(url, data=body, headers=headers)
    return data.json()