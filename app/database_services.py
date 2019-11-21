from app.models import FaScrape, Artist
from app.constants import EnvConstants as ec
from datetime import datetime
from app.database import db_session


class DBServices(object):

    def db_add_artists_names(self, names_dict):
        db = db_session()
        art = Artist()
        for art_entry in names_dict:
            user_name = art_entry['user_name']
            artist_full_path = art_entry['user_path']
            db.execute("""
            INSERT INTO public.artists (artist_name, follows, artist_full_path)
            VALUES ( '{}',{},'{}' )""".format(user_name, True, artist_full_path))
            db.commit()

    def db_get_artist(self):
        pass

    def db_update_artist_info(self):
        pass
