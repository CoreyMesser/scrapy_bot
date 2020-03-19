from scraper_services import WatchList, ArtistInfo
from database_services import DBServices
from auth_services import Auth
from aws_services import AWSServices

from logger import LoggerService

ls = LoggerService()
_log = ls.get_logger()


class Processors(object):

    def add_update_artists(self):
        wl = WatchList()
        ds = DBServices()

        _log.info('Scrape Started')
        watch_list = wl.soup_parser()
        _log.info('Soup Started')
        names_dict = wl.soup_dict(watch_list=watch_list)
        _log.info('Comparing')
        artist_dict = ds.db_artist_check(watch_dict=names_dict)
        _log.info('Updating DB')
        ds.db_add_artists_names(names_dict=artist_dict)
        _log.info('Checking Unfollows')
        ds.get_artist_integrity(current_list=names_dict)
        _log.info('FIN')

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
        _log.info('Artist Update Started')
        session = self.login()
        _log.info('Log in Successful')
        artist_list = ds.db_get_artists_social_update()
        _log.info('Artists List Retreived')
        for user in artist_list:
            user_dict = ai.artist_processor(session=session, user=user)
            ds.db_update_artist_info(user_dict=user_dict)
        _log.info('FIN')

    def send_twitter_list_s3(self):
        ds = DBServices()
        awss = AWSServices()
        _log.info('Pulling latest list')
        user_list = ds.get_twitter_list()
        _log.info('Creating CSV')
        csv_file = ds.df_to_csv_to_s3(data=user_list)
        _log.info('Sending CSV to s3')
        awss.s3_send_list(csv_file=csv_file)
        _log.info('FIN')

    def test_check(self):
        wl = WatchList()
        ds = DBServices()
#
#
# if __name__ == '__main__':
#     p = Processors()
#     p.add_update_artists()
