from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm
from time import sleep
from decouple import config
time_input = input("Which year do you wnat to travel to? Type the date in this format YYYY-MM-DD: ")
url = f"https://www.billboard.com/charts/hot-100/{time_input}"
billboard_site = requests.get(url=url).text
soup = BeautifulSoup(billboard_site, "html.parser")
title_tags = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
artist_tag = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
song_title_list = [tag.getText() for tag in title_tags]
song_artist_list = [artist.getText() for artist in artist_tag]
# print(song_title_list)
# print(song_artist_list)

# -------------------- Spotify Handeler -------------------- #
CLIENT_ID = config("CLIENT")
CLIENT_SECRET = config("CLIENT_SECRET")
client = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = client.current_user()["id"]
# print(user_id)
year = time_input.split('-')[0]
song_link = client.search(q=f"track: {'All I Want For Christmas Is You'}")["tracks"]["items"][0]["external_urls"][
    "spotify"]
song_links = []
for title in song_title_list:
    try:
        song_link = client.search(q=f"track: {title}")["tracks"]["items"][0]["external_urls"]["spotify"]
    except IndexError:
        pass
        # print(f"{title} is Not available")
    else:
        song_links.append(song_link)

play_list_data = client.user_playlist_create(
    user=user_id,
    name=f"{time_input} Billboard 100!",
    public=False,
    description=f"A collection of the 100 most songs from Billboard.com for {time_input}")
play_list_id = play_list_data["id"]
client.playlist_add_items(playlist_id=play_list_id, items=song_links)

# tqdm control
for _ in tqdm(range(0, 100), total=100, desc="Working on it! "):
    sleep(0.1)


print(f"Here is the playlist's link: {play_list_data['external_urls']['spotify']}\nEnjoy!")
