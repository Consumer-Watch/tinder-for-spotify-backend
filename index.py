from flask import Flask, request, redirect, jsonify
from spotify_config import spotify
import requests
import os

app = Flask(__name__)

file_write = open("tokens.txt", "a")

@app.route('/login', methods=["GET"])
def index_route():

    url = "https://accounts.spotify.com/authorize" 
     # replace with your actual API endpoint
    body = { 
        "client_id": os.getenv("CLIENT_ID"),   
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": "http://localhost:5000/profile",
        "scope": "user-read-private user-read-email user-top-read",
        "response_type": "code"
    }  # replace with your actual request body
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "grant_type": "refresh_token"
    }
    data = requests.get(url, params=body, headers=headers)
    print(data.url)
    return jsonify({ "url": data.url })

@app.route('/profile')
def profile():
    code = request.args.get("code")
    data = spotify(code)
    print (data)
    file_write.write(f'''
Access Token:{data['access_token']}
Refresh Token:{data['refresh_token']}
                     ''')
    file_write.close()
    return jsonify(data) #client should store this

@app.route('/me')
def me_route():
    request.headers.get("")
    headers = {
        "Authorization": "Bearer BQAbTaShrjpuLdmlTlQ74rikYv2u1b4GylYehdLmeSileiGdxcWwTFiCe-VrI3apoGEA_7pHdK1Yk6k5Ghidiokfn31L8CDhSfOJHQVyCh0geOpuhxX38BfVON6yHJUGEi_pDoNNQ2RwXJUnMOZRaUewSPsyVZ81qbv1e-BUf36FadvuVVjCEWDx2efhe338n8YUx3wYL788byHfyYDS5x32mo4"
    }
    data = requests.get("https://api.spotify.com/v1/me", headers=headers)
    data2 = requests.get("https://api.spotify.com/v1/me/top/artists", headers=headers)
    return jsonify(data2.json())

if __name__ == "__main__":
    app.run(debug=True)