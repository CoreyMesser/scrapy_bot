import requests
from requests import session

import cfscrape
import bs4
from lxml import html

from app.constants import EnvConstants as ec

class Auth(object):

    def __init__(self, useragent=None, session=None):
        payload = {
            'username': ec.TARGET_USER,
            'password': ec.TARGET_PW,
            '_cfduid': ec.CF_DUID,
            'a': ec.CF_A,
            'b': ec.CF_B,
        }

        self.session = requests.session()
        self.logged_in = False

        self.headers = {'User-Agent': ec.HEADERS,
                        'Connection': 'keep-alive'}
        try:
            self.scraper = cfscrape.CloudflareScraper()
            self.scraper.post(ec.TARGET_SITE, data=payload)
        except Exception as e:
            print(f'Failed due to {e}')


