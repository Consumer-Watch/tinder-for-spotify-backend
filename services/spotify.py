import requests

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
            "artists": [artist['name'] for artist in artists] if artists else [episode_publisher]
        }
