import requests

import cfscrape
import bs4

from app.constants import EnvConstants as ec

class Auth(object):

    def __init__(self):
        self.session = requests.session()
        self.session = cfscrape.create_scraper(self.session, delay=10)

    def login(self):

        try:
            payload = {
                'username': ec.TARGET_USER,
                'password': ec.TARGET_PW,
            }

            cookies_dict = {
                'a': ec.CF_A,
                'b': ec.CF_B,
                '__cfduid': ec.CF_DUID
            }

            headers = {'User-Agent': ec.HEADERS,
                       'Connection': 'keep-alive'
                       }

            del self.session.cookies['__cfduid']

            self.session.post(ec.TARGET_SITE, data=payload, headers=headers, cookies=cookies_dict)
            return self.session
        except Exception as e:
            print(f'Failed due to {e}')

    def check_login(self):
        response = self.session.get(ec.TARGET_SITE)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        user_link = soup.find("a", id="my-username")
        if user_link:
            logged_in = True
            print('Logged In')
        else:
            logged_in = False
        return logged_in


