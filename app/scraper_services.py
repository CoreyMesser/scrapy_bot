import scrapy
import os
import cfscrape
import requests
import re
from bs4 import BeautifulSoup
import html.parser

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
        # pull tokens from DB
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

    #db passes in path to assemble path

    def asemble_path(self, path):
        return ec.TARGET_SITE + '/' + ec.PATH_USER + path

    def artist_soup_parser(self):
        social_list = []
        #calls wl.cfscrape
        req = self.cf_scrape(path=path)
        soup = BeautifulSoup(req.content, 'html.parser')
        social_list.append(list(soup.find("a", href=re.compile("http://www.twitter.com/"))))
        social_list.append(list(soup.find("a", href=re.compile("https://t.me/"))))
