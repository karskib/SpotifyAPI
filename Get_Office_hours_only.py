import requests
import json
import sys
from settings import Settings


class Spotify:

    def __init__(self):
        self.token_data = {
            'grant_type': 'client_credentials',
        }
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.client_id = Settings.client_id
        self.client_secret = Settings.client_secret
        self.show_id = Settings.show_id
        self.tk = Settings.tk
        self.tracks = Settings.tracks
        self.username = Settings.username
        self.headers = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {self.tk}"}


    def get_episodes_ids(self):
        link = 'https://api.spotify.com/v1/shows/{}?market=PL'.format(self.show_id)
        r = requests.get(link, headers=self.headers)
        r_json = r.json()
        episodes = r_json['episodes']['items']
        for episode in episodes:
            if 'office hours' in episode['name'].lower():
                self.tracks += (episode['uri'] + ',')
        self.tracks = self.tracks[:-1]
        return self.tracks

    def create_playlist(self):
        ref = f'https://api.spotify.com/v1/users/{self.username}/playlists'
        get_playlists_names = requests.get(ref, headers=self.headers)
        get_playlists_names_json = get_playlists_names.json()
        for item in get_playlists_names_json['items']:
            if item['name'] in [i.lower() for i in ['office_hours']]:
                print('this playlist already exists')
                sys.exit('Exiting the program')
            else:
                body = json.dumps({
                    "name": "office_hours",
                    "description": "Prof G's only office hours",
                    "public": True})
                r = requests.post(ref, data=body, headers=self.headers)
                r_json = r.json()
                print(r, f'playlist created')
                return r_json['id']

    def add_office_hours_only(self):
        print('adding episodes to the playlist..')
        url = f'https://api.spotify.com/v1/playlists/{self.create_playlist()}/tracks?uris={self.get_episodes_ids()}'
        req = requests.post(url, headers=self.headers)
        print(req, 'Episodes have been successfully added..')


if __name__ == '__main__':
    s = Spotify()
    s.add_office_hours_only()
