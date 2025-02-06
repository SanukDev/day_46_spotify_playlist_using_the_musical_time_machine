from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

CLIENT_ID = "YOUR ID"
CLIENT_SECRET = "YOUR SECRET"

URL = "https://www.billboard.com/charts/hot-100/"
year = int(input("Type the year that you would like hear the hot 100 music"))
month = int(input("Type the mouth as well"))
day = int(input("Type the day too"))
response = requests.get(f"{URL}{year}-{month}-{day}")

data = response.text

soup = BeautifulSoup(data, "html.parser")

title_music = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                              "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                              "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                                              "u-max-width-230@tablet-only")

song_names_spans = soup.select("li ul li h3")

songs = [song.getText().split() for song in song_names_spans]
songs_update = []
str_songs = ""
for song_for in songs:
    for song_two_for in song_for:
        str_songs += song_two_for + " "
    songs_update.append(str_songs)
    str_songs = ""
date = f"{year}-{month}-{day}"
# ----------------------------------------------------  Spotify API ----------------------------------------------------
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://developer.spotify.com/dashboard",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt", #YOUR TOKEN HERE---------
        username="samukakaroto",
    )
)

user_id = sp.current_user()["id"]
song_uris = []
print(date)

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date}-Samuel",
    public=False
)

for song in songs_update:
    result = sp.search(q=f"track:{song}", type="track", limit=30)
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

        print(song)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

sp.playlist_add_items(
            playlist_id=playlist["id"],
            items=song_uris
        )
