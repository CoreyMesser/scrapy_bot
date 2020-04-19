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
        """
        simply pings tirefire to see if still burning
        :return:
        """
        site_ping = requests.get(url=ec.TARGET_SITE)
        return {'code': site_ping.status_code, 'message': site_ping.url}

    def ping_user(self):
        """
        simply pings user to see if exists
        :return:
        """
        user_ping = requests.get(url=ec.TARGET_SITE + '/' + ec.PATH_USER + '/' + ec.TARGET_USER)
        return {'code': user_ping.status_code, 'message': user_ping.url}


class WatchList(scrapy.Spider):
    name = 'watchers'

    cf_delay = 10
    session = requests.session()
    session.headers = []
    user_path = ec.TARGET_SITE + '/' + ec.PATH_USER + '/'
    user_watch_path = ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/'
    user_watching_path = ec.TARGET_SITE + '/' + ec.PATH_WATCHING + '/' + ec.TARGET_USER + '/'

    def cf_get_tokens(self):
        """
        gets login token
        :return:
        """
        dblist = 'dblist_sql'
        if dblist:
            sql = 'sql'
        else:
            cfscrape.get_cookie_string()
        pass

    def cf_login(self):
        pass

    def cf_scrape(self, path):
        """
        scraper service
        :param path:
        :return:
        """
        scraper = cfscrape.create_scraper(delay=self.cf_delay)
        req = scraper.get(path)
        return req

    def scrape_user(self, username: str):
        """
        scrapes user stats
        :param username:
        :return:
        """
        path = self.user_path + username
        soup = self.soup_parser(path=path)
        return self.scrape_stats(soup)

    def scrape_stats(self, soup):
        stats = list(soup.find_all("div", attrs={'class': 'cell'}))
        watches = list(soup.find_all(href=re.compile("/watchlist/")))
        user_model = {'views': 0,
                      'faves': 0,
                      'watchers': 0,
                      'watching': 0}
        if len(stats) >= 1 and len(watches) >= 1:
            try:
                user_model['views'] = int(stats[0].contents[2])
            except IndexError:
                _log.error(f"[ERROR][SCRAPE STATS] Tirefire views")
            try:
                user_model['faves'] = int(stats[0].contents[10])
            except IndexError:
                _log.error(f"[ERROR][SCRAPE STATS] Tirefire faves")
            user_model['watchers'] = self.strip_watcher_values(watches=watches[0].contents[0])
            user_model['watching'] = self.strip_watcher_values(watches=watches[1].contents[0])
        else:
            _log.error("[ERROR][SCRAPE USER] No stats generated...")
        return user_model

    def strip_watcher_values(self, watches):
        """
        since its a tirefire of a site they mangled their stats, this strips the number out of the string
        :param watches:
        :return:
        """
        return int(re.findall(r'[0-9]+', watches)[0])

    def calculate_watch_num_pages(self, watchers):
        """calculates number of watch pages"""
        return int(watchers / 200)

    def get_path(self, watch):
        """
        gets number of users, calculates pages, and builds a list of paths to consumption
        :param watch:
        :return:
        """
        user_model = self.scrape_user(username=ec.TARGET_USER)
        pages = self.calculate_watch_num_pages(watchers=user_model['watchers'])
        core_path = ec.TARGET_SITE + '/' + watch + '/' + ec.TARGET_USER + '/'
        page = 1
        path_list = []
        while page <= pages:
            path_list.append(core_path + str(page) + '/')
            page += 1
        return path_list

    def soup_watchlist_parser(self, watch):
        """
        uses the path list to strip out the users from each page
        :param watch:
        :return:
        """
        raw_watchlist = []
        pathes = self.get_path(watch=watch)
        _log.info('[ADD UPDATE] Paths Complete')
        for path in pathes:
            soup = self.soup_parser(path)
            raw_watchlist.append(list(soup.find_all("a", href=re.compile("/user/"))))
        _log.info('[ADD UPDATE] Watchlist Complete')
        return raw_watchlist

    def soup_parser(self, path):
        """
        soup parser service
        :param path:
        :return:
        """
        req = self.cf_scrape(path=path)
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup

    def soup_dict(self, watch_list):
        """
        creates a dictionary out of the cleaned usernames
        :param watch_list:
        :return:
        """
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
        """
        path assembler, pass in username and returns a completed path for consumption
        :param user:
        :return:
        """
        return ec.TARGET_SITE + '/' + user

    def unwatch_user(self, session, response):
        """
        unwatches user from tirefire
        :param session:
        :param response:
        :return:
        """
        soup = BeautifulSoup(response.text, "html.parser")
        unwatch_link = soup.find_all("a", href=re.compile("/unwatch/"))
        session.get(unwatch_link.attrs['href'])
        _log.info('[ARTIST INFO] User unwatched')

    def user_active(self, session, response):
        """
        checks to see if the user is active or inactive returns bool
        :param session:
        :param response:
        :return:
        """
        user_active = True
        soup = BeautifulSoup(response.text, "html.parser")
        user_check = soup.title.string
        if user_check == ec.ACC_DISABLED:
            user_active = False
        return user_active

    def artist_soup_parser(self, response):
        """
        strips out twitter and telegram links from user's profile
        :param response:
        :return:
        """
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

    def artist_stats(self, response):
        wl = WatchList()
        soup = BeautifulSoup(response.content, 'html.parser')
        user_model = wl.scrape_stats(soup=soup)
        return user_model

    def artist_processor(self, session, user):
        """
        main processing tree for artists, assembles path, checks active, assembles dict of social links
        :param session:
        :param user:
        :return:
        """
        user_dict = {}
        user_dict['full_path'] = user[0]
        path = self.assemble_path(user=user_dict['full_path'])
        response = session.get(url=path)
        user_dict['active'] = self.user_active(session=session, response=response)
        telegram, twitter = self.artist_soup_parser(response=response)
        user_dict['telegram'] = telegram
        user_dict['twitter'] = twitter
        user_stats = self.artist_stats(response=response)
        return user_dict, user_stats
