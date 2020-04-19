from scraper_services import WatchList, ArtistInfo, HealthChecks
from run import Processors

from logger import LoggerService

ls = LoggerService()
_log = ls.get_logger()
wl = WatchList()
hc = HealthChecks()
pr = Processors()

def ping_site():
    _log.info('Pinging Site')
    return hc.ping_site()


def ping_user():
    _log.info('Pinging User')
    return hc.ping_user()


def get_users():
    pass


def scrape_user(username: str):
    return wl.scrape_user(username)


def update_users():
    return pr.add_update_artists()


def update_social():
    return pr.social_update(None)


def send_s3():
    return pr.send_twitter_list_s3()

def update_stats():
    return pr.update_stats()

def update_watching():
    return pr.add_update_watching()
