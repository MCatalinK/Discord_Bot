import os
import requests
from dotenv import load_dotenv


class GifConfiguration:
    # GifToken = '0K1EXNI58T61'
    load_dotenv()
    GifToken = os.getenv('GIF')
    limit = 1

    def __init__(self, search_term):
        self.search_term = search_term

    def get_gif(self):
        r = requests.get(
            "https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (self.search_term, self.GifToken, self.limit))

        if r.status_code == 200:
            data = r.json()
        else:
            data = None
            return data

        return data['results'][0]['media'][0]['gif']['url']
