import scrapy
import cfscrape
import requests
import re
from bs4 import BeautifulSoup

from app.constants import EnvConstants as ec


class WatchList(scrapy.Spider):
    name = 'watchers'

    path = ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/'

    cf_delay = 10
    session = requests.session()
    session.headers  = []

    def get_path(self):
        path = [ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '2' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '3' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '4' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '5' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '6' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '7' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '8' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '9' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '10' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '11' + '/',
        ]
        return path

    def cf_get_tokens(self):
        dblist = 'dblist_sql'
        if dblist:
            sql = 'sql'
        else:
            cfscrape.get_cookie_string()
        pass

    def cf_login(self):
        pass

    def cf_scrape(self, path):
        scraper = cfscrape.create_scraper(delay=self.cf_delay)
        req = scraper.get(path)
        return req

    def soup_parser(self):
        raw_watchlist = []
        pathes = self.get_path()
        print('Pathes Complete')
        for path in pathes:
            req = self.cf_scrape(path=path)
            soup = BeautifulSoup(req.content, 'html.parser')
            raw_watchlist.append(list(soup.find_all("a", href=re.compile("/user/"))))
        print('Watchlist Complete')
        return raw_watchlist

    def soup_dict(self, watch_list):
        watch_dict = []
        for chunk in watch_list:
            for entry in chunk:
                user_path = entry.attrs['href']
                user_name = entry.string
                watch_dict.append({'user_name': user_name, 'user_path': user_path})
        print('Dict Complete')
        return watch_dict


class ArtistInfo(scrapy.Spider):
    name = "watchers"

    def assemble_path(self, user):
        return ec.TARGET_SITE + '/' + user

    def unwatch_user(self, session, response):
        soup = BeautifulSoup(response.text, "html.parser")
        unwatch_link = soup.find_all("a", href=re.compile("/unwatch/"))
        session.get(unwatch_link.attrs['href'])

    def user_active(self, session, response):
        soup = BeautifulSoup(response.text, "html.parser")
        user_check = soup.title.string
        if user_check == ec.ACC_DISABLED:
            user_active = False
            # self.unwatch_user(session=session, response=response)
        else:
            user_active = True
        return user_active

    def artist_soup_parser(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            tw_link = soup.find("a", href=re.compile("http://www.twitter.com/"))
            twitter_link = tw_link.attrs['href']
        except:
            twitter_link = None
        try:
            tel_link = soup.find("a", href=re.compile("https://t.me/"))
            telegram_link = tel_link.attrs['href']
        except:
            telegram_link = None
        return telegram_link, twitter_link

    def artist_processor(self, session, user):
        user_dict = {}
        user_dict['full_path'] = user[0]
        path = self.assemble_path(user=user_dict['full_path'])
        response = session.get(url=path)
        user_dict['active'] = self.user_active(session=session, response=response)
        telegram, twitter = self.artist_soup_parser(response=response)
        user_dict['telegram'] = telegram
        user_dict['twitter'] = twitter
        return user_dict
