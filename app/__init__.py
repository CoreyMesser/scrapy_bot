from app.scraper_services import WatchList
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
        a.__init__()


if __name__ == '__main__':
    p = Processors()
    p.initial_add_artists()
