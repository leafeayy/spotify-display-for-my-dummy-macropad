from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get

# Load environment variables
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Token request failed: {response.status_code}, {response.text}")
    return response.json()["access_token"]

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def get_album_details(album_id, token):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    response = get(url, headers=headers)
    if response.status_code != 200:
        print(f"Album details fetch failed: {response.status_code}")
        print(response.text)
        return None
    return response.json()

def format_duration(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    return f"{minutes}:{seconds:02}"

# Main logic
if __name__ == "__main__":
    try:
        token = get_token()
        album_name = "..."  
        album = search_album(album_name, token)

        if not album:
            print("Album not found.")
        else:
            album_id = album["id"]
            details = get_album_details(album_id, token)

            print(f"\nAlbum: {details['name']}")
            print(f"Artist: {details['artists'][0]['name']}")
            print(f"Release Date: {details['release_date']}")
            print(f"Cover: {details['images'][0]['url']}\n")

            print("Track List:")
            for idx, track in enumerate(details["tracks"]["items"], 1):
                track_name = track["name"]
                duration = format_duration(track["duration_ms"])
                print(f"{idx}. {track_name} ({duration})")

    except Exception as e:
        print("Error:", e)
