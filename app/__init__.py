from app.scraper_services import WatchList, ArtistInfo
from app.database_services import DBServices
from app.auth_services import Auth


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





if __name__ == '__main__':
    p = Processors()
    p.social_update()
