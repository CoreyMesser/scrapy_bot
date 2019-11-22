import requests
from requests import session

from http import cookiejar
from http.cookiejar import Cookie

import cfscrape
import bs4
from lxml import html

from app.constants import EnvConstants as ec

class Auth(object):

    def __init__(self):
        self.session = requests.session()
        self.session = cfscrape.create_scraper(self.session)

    def login(self):

        try:
            # jar = cookiejar.CookieJar()
            # jar.add_cookie_header(Cookie(name='__cfduid',
            #                       value=ec.CF_DUID,
            #                       comment=None,
            #                       comment_url=None,
            #                       discard=False,
            #                       domain=ec.TARGET_SITE,
            #                       domain_initial_dot=False,
            #                       domain_specified=ec.TARGET_SITE,
            #                       expires=None,
            #                       path='/',
            #                       path_specified='/',
            #                       port=443,
            #                       port_specified=443,
            #                       rfc2109=False,
            #                       rest={'HttpOnly': None},
            #                       secure=False,
            #                       version=1))
            #
            # cf_cookie = Cookie(name='__cfduid',
            #                       value=ec.CF_DUID,
            #                       comment=None,
            #                       comment_url=None,
            #                       discard=False,
            #                       domain=ec.TARGET_SITE,
            #                       domain_initial_dot=False,
            #                       domain_specified=ec.TARGET_SITE,
            #                       expires=None,
            #                       path='/',
            #                       path_specified='/',
            #                       port=443,
            #                       port_specified=443,
            #                       rfc2109=False,
            #                       rest={'HttpOnly': None},
            #                       secure=False,
            #                       version=1)

            cookie_dict = {
                'name': '__cfduid',
                'value': ec.CF_DUID,
                'comment': None,
                'comment_url': None,
                'discard': False,
                'domain': ec.TARGET_SITE,
                'expires': None,
                'path': '/',
                'port': 443,
                'rfc2109': False,
                'rest': {
                'HttpOnly': None},
                'version': 0
            }

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


