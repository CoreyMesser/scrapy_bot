from app.scraper_services import WatchList, ArtistInfo
from app.database_services import DBServices
from app.auth_services import Auth
from app.aws_services import AWSServices


class Processors(object):

    def initial_add_artists(self):
        wl = WatchList()
        ds = DBServices()

        print('Scrape Started')
        watch_list = wl.soup_parser()
        names_dict = wl.soup_dict(watch_list=watch_list)
        ds.db_add_artists_names(names_dict=names_dict)
        print('FIN')

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
        print('Artist Update Started')
        session = self.login()
        print('Log in Successful')
        artist_list = ds.db_get_artists()
        print('Artists List Retreived')
        for user in artist_list:
            user_dict = ai.artist_processor(session=session, user=user)
            ds.db_update_artist_info(user_dict=user_dict)
        print('FIN')

    def send_twitter_list_s3(self):
        ds = DBServices()
        awss = AWSServices()
        print('Pulling latest list')
        user_list = ds.get_twitter_list()
        print('Creating CSV')
        csv_file = ds.df_to_csv_to_s3(data=user_list)
        print('Sending CSV to s3')
        awss.s3_send_list(csv_file=csv_file)
        print('FIN')

if __name__ == '__main__':
    p = Processors()
    p.send_twitter_list_s3()
