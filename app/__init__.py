from app.scraper_services import WatchList
from app.database_services import DBServices



if __name__ == '__main__':
    wl = WatchList()
    ds = DBServices()

    print('Scrape Started')
    watch_list = wl.soup_parser()
    names_dict = wl.soup_dict(watch_list=watch_list)
    ds.db_update_artists_names(names_dict=names_dict)
    print('FIN')
