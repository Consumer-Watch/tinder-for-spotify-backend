import requests
from utils.responses import success_response

def get_top_items_from_api(access_token: str, type: str) -> list[dict[str, any]]:
    params = {
        "limit": 10,
        "offset": 0,
        "time_range": "medium_term"
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }


    url = f"https://api.spotify.com/v1/me/top/{type}"
    response = requests.get(url=url, params=params, headers=headers)
    top_items = response.json()
    top_items = top_items["items"]

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

