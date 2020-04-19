from scraper_services import WatchList, ArtistInfo
from database_services import DBServices
from auth_services import Auth
from aws_services import AWSServices
from constants import EnvConstants as ec

from logger import LoggerService

ls = LoggerService()
_log = ls.get_logger()


class Processors(object):

    def add_update_artists(self):
        wl = WatchList()
        ds = DBServices()
        watched = ec.PATH_WATCHLIST

        _log.info('[ADD UPDATE USERS] Scrape Started')
        watch_list = wl.soup_watchlist_parser(watch=watched)
        _log.info('[ADD UPDATE USERS] Soup Started')
        names_dict = wl.soup_dict(watch_list=watch_list)
        _log.info('[ADD UPDATE USERS] Comparing')
        artist_dict = ds.db_artist_check(watch_dict=names_dict, watch=watched)
        _log.info('[ADD UPDATE USERS] Updating DB')
        ds.db_add_artists_names(names_dict=artist_dict)
        _log.info('[ADD UPDATE USERS] Checking Unfollows')
        ds.get_artist_integrity(current_list=names_dict)
        _log.info('[ADD UPDATE USERS] FIN')
        return "Watchers have been updated."

    def login(self):
        a = Auth()
        if a.check_login() == False:
            session = a.login()
        else:
            session = a.session
        return session

    def social_update(self):
        ds = DBServices()
        ai = ArtistInfo()
        _log.info('[SOCIAL UPDATE] Artist Update Started')
        session = self.login()
        _log.info('[SOCIAL UPDATE] Log in Successful')
        artist_list = ds.db_get_artists_social_update()
        _log.info('[SOCIAL UPDATE] Artists List Retreived')
        for user in artist_list:
            _log.info('[SOCIAL UPDATE] Processing artist')
            user_dict = ai.artist_processor(session=session, user=user)
            ds.db_update_artist_info(user_dict=user_dict)
            _log.info('[SOCIAL UPDATE] Artist Processed')
        _log.info('[SOCIAL UPDATE] FIN')
        return "Social has been updated"

    def send_twitter_list_s3(self):
        ds = DBServices()
        awss = AWSServices()
        _log.info('[SEND TO S3] Pulling latest list')
        user_list = ds.get_twitter_list()
        _log.info('[SEND TO S3] Creating CSV')
        csv_file = ds.df_to_csv_to_s3(data=user_list)
        _log.info('[SEND TO S3] Sending CSV to s3')
        awss.s3_send_list(csv_file=csv_file)
        _log.info('[SEND TO S3] FIN')
        return "List has been sent to s3"

    def update_stats(self):
        ds = DBServices()
        wl = WatchList()
        _log.info('[UPDATE STATS] Scraping User')
        stats_dict = wl.scrape_user(username=ec.TARGET_USER)
        _log.info('[UPDATE STATS] Stats retrieved')
        ds.db_update_stats(stats_dict=stats_dict)
        _log.info('[UPDATE STATS] User stats updated')
        return "Stats have been updated!"

    def add_update_watching(self):
        wl = WatchList()
        ds = DBServices()
        watching = ec.PATH_WATCHING

        _log.info('[ADD UPDATE USERS] Scrape Started')
        watch_list = wl.soup_watchlist_parser(watch=watching)
        _log.info('[ADD UPDATE USERS] Soup Started')
        names_dict = wl.soup_dict(watch_list=watch_list)
        _log.info('[ADD UPDATE USERS] Comparing')

        artist_dict = ds.db_artist_check(watch_dict=names_dict, watch=watching)
        _log.info('[ADD UPDATE USERS] Updating DB')

        ds.db_add_artists_names(names_dict=artist_dict)
        _log.info('[ADD UPDATE USERS] Checking Unfollows')
        ds.get_artist_integrity(current_list=names_dict)
        _log.info('[ADD UPDATE USERS] FIN')
        return "Watchers have been updated."

