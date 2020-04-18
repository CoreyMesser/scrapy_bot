import scrapy
import cfscrape
import requests
import re
from bs4 import BeautifulSoup

from app.constants import EnvConstants as ec
from app.logger import LoggerService

ls = LoggerService()
_log = ls.get_logger()


class HealthChecks(object):

    def ping_site(self):
        site_ping = requests.get(url=ec.TARGET_SITE)
        return {'code': site_ping.status_code, 'message': site_ping.url}

    def ping_user(self):
        user_ping = requests.get(url=ec.TARGET_SITE + '/' + ec.PATH_USER + '/' + ec.TARGET_USER)
        return {'code': user_ping.status_code, 'message': user_ping.url}


class WatchList(scrapy.Spider):
    name = 'watchers'

    cf_delay = 10
    session = requests.session()
    session.headers = []
    user_path = ec.TARGET_SITE + '/' + ec.PATH_USER + '/'
    user_watch_path = ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/'

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

    def scrape_user(self, username: str):
        user_model = {'views':0,
                      'faves':0,
                      'watchers':0,
                      'watching':0}
        path = self.user_path + username
        soup = self.soup_parser(path=path)
        stats = list(soup.find_all("div", attrs={'class': 'cell'}))
        watches = list(soup.find_all(href=re.compile("/watchlist/")))
        if len(stats) >= 1 and len(watches) >= 1:
            user_model['views'] = int(stats[0].contents[2])
            user_model['faves'] = int(stats[0].contents[10])
            user_model['watchers'] = self.strip_watcher_values(watches=watches[0].contents[0])
            user_model['watching'] = self.strip_watcher_values(watches=watches[1].contents[0])
        else:
            user_model = f"No results found, Username : {username} may be incorrect"
        return user_model

    def strip_watcher_values(self, watches):
        return int(re.findall(r'[0-9]+', watches)[0])

    def calculate_watch_num_pages(self):
        """calculates number of watch pages"""
        total_watchers = 0
        return int(total_watchers / 200)

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
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '12' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '13' + '/'
                ]
        return path

    def soup_watchlist_parser(self):
        raw_watchlist = []
        pathes = self.get_path()
        _log.info('Pathes Complete')
        for path in pathes:
            soup = self.soup_parser(path)
            raw_watchlist.append(list(soup.find_all("a", href=re.compile("/user/"))))
        _log.info('Watchlist Complete')
        return raw_watchlist

    def soup_parser(self, path):
        req = self.cf_scrape(path=path)
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup

    def soup_dict(self, watch_list):
        watch_dict = []
        for chunk in watch_list:
            for entry in chunk:
                user_path = entry.attrs['href']
                user_name = entry.string
                watch_dict.append({'user_name': user_name, 'user_path': user_path})
        _log.info('Dict Complete')
        return watch_dict


class ArtistInfo(scrapy.Spider):
    name = "watchers"

    def assemble_path(self, user):
        return ec.TARGET_SITE + '/' + user

    def unwatch_user(self, session, response):
        soup = BeautifulSoup(response.text, "html.parser")
        unwatch_link = soup.find_all("a", href=re.compile("/unwatch/"))
        session.get(unwatch_link.attrs['href'])
        _log.info('User unwatched')

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
