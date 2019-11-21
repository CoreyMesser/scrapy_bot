import scrapy
import os
import cfscrape
import requests
from bs4 import BeautifulSoup

from app.constants import EnvConstants as ec


class WatchList(scrapy.Spider):
    name = 'watchers'

    path = ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/'

    cf_delay = 10
    session = requests.session()
    session.headers  = []

    def get_path(self):
        path = ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/'
        return path

    def start_requests(self):
        urls = [
            self.watchlist_path + '/' + '1',
            self.watchlist_path + '/' + '2'
        ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

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

    def cf_scrape(self):
        scraper = cfscrape.create_scraper(delay=self.cf_delay)
        path = self.get_path()
        req = scraper.get(path)
        return req

    def soup_parser(self):
        req = self.cf_scrape()
        soup = BeautifulSoup(req)
        raw_watchlist = soup.td
