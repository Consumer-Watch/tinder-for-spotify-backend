from os import getenv
import requests
from collections import Counter
from functools import lru_cache
from config.app import app

from validators.spotify import SpotifyError, raise_error

class SpotifyService:
    base_url = "https://api.spotify.com/v1"


    @classmethod
    def currently_playing_track(cls, authorization: str, country: str):
        url = f"{cls.base_url}/me/player/currently-playing"
        header = {
            "Authorization": authorization
        }
        params = { "market": country }
        response = requests.get(url=url, headers=header, params=params)
        currently_playing = response.json()
        
        raise_error(currently_playing)
        devices_url = f"{cls.base_url}/me/player/devices"
        devices_response = requests.get(url=devices_url, headers=header)
        devices = devices_response.json().get('devices', None)

        active_device = next((device for device in devices if device['is_active']), None)

        audio_item = currently_playing["item"]

        image = audio_item['images'][0]['url'] if audio_item.get('images', None) else audio_item['album']['images'][0]['url']
        artists = audio_item.get("artists", None) if audio_item.get("artists", None) else None

        episode_publisher = audio_item.get('show', None)['publisher'] if audio_item.get('oublisher', None) else None

        return {
            "progress": currently_playing["progress_ms"],
            "is_playing": currently_playing["is_playing"],
            "name": audio_item["name"],
            "duration": audio_item["duration_ms"],
            "image": image,
            "device": {
                "name": active_device["name"],
                "type": active_device["type"]
            },
            "artists": [artist['name'] for artist in artists] if artists else [episode_publisher]
        }
    
    @classmethod
    def get_top_items(cls, authorization: str, type: str) -> list[dict[str, any]]:
        params = { "limit": 15, "offset": 0, "time_range": "medium_term" }
        headers = { "Authorization": authorization }

        url = f"{cls.base_url}/me/top/{type}"
        response = requests.get(url=url, params=params, headers=headers)
        response_data = response.json()
        raise_error(response_data)

        top_items = response_data["items"]

        #change this from top_artists
        if type == "artists":
            items = [{
                "name": item["name"], 
                "image": item['images'][-1]['url'] if item['images'] else None, 
                "id": item["id"], 
                "position": index + 1,

            } for index, item in enumerate(top_items)]
    
        elif type == "tracks":
            items = [{
                "name": item["name"], 
                "image": item['album']['images'][1]['url'] if item['album']['images'] else None, 
                "id": item["id"], 
                "position": index+1,
                "preview_url": item["preview_url"],
                "artists": [{ 
                    "id": artist["id"], 
                    "name": artist["name"],
                    "image": ""
                } for artist in item["artists"]] if item["artists"] else None

            } for index, item in enumerate(top_items)]

        else:
            items = []        
    
        return items
    
    @classmethod
    def get_top_items_genres(cls, authorization: str) -> list[str]:
        @lru_cache(maxsize=128)  # Adjust maxsize as needed
        def _cached_get_top_items_genres(auth: str):
            params = { "limit": 15, "offset": 0, "time_range": "medium_term" }
            headers = { "Authorization": authorization }

            url = f"{cls.base_url}/me/top/artists" 
            response = requests.get(url=url, params= params, headers=headers)
         # Check if the response status code indicates success
            if response.status_code == 200:
                try:
                    top_artists = response.json()["items"]
                except ValueError:
            # Handle cases where the response is not in JSON format
                    return f"Error parsing JSON from response: {response.text}"
            else:
        # Log or handle unsuccessful response
                return f"Request failed with status code: {response.status_code}, response: {response.text}"
        
       
            genre_counter = Counter()
            for item in top_artists:
                if "genres" in item:
                    genre_counter.update(item["genres"])
 
            top_genres = genre_counter.most_common(6)
            top_genres_without_count = [genre[0] for genre in top_genres if genre]
            return top_genres_without_count
        return _cached_get_top_items_genres(authorization)
    
    
    @classmethod
    def get_credentials(cls, code: str):
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
    
    @classmethod
    def renew_token(cls, refresh_token: str):
        url = "https://accounts.spotify.com/api/token" 

        body = { 
            "refresh_token": refresh_token,   
            "grant_type": "refresh_token",
            "client_id": getenv("CLIENT_ID"),
            "client_secret": getenv("CLIENT_SECRET"),

        } 
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        data = requests.post(url, data=body, headers=headers)
        return data.json();

    @classmethod
    def get_current_user(cls, authorization: str):
        headers = { "Authorization": authorization }
        response = requests.get(f"{cls.base_url}/me", headers=headers)
        response_data = response.json()
        raise_error(response_data)

        return response_data




