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
    print(top_items, "items")
    top_items = top_items["items"]

    #change this from top_artists
    top_artists = [{"name": item["name"], "image": item['images'][-1]['url'] if item['images'] else None, "id": item["id"], "position": index+1 } for index, item in enumerate(top_items)]
    return top_artists

