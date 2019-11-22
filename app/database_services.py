from app.models import FaScrape, Artist
from app.constants import EnvConstants as ec
from datetime import datetime
from app.database import db_session


class DBServices(object):

    def db_add_artists_names(self, names_dict):
        db = db_session()
        for art_entry in names_dict:
            user_name = art_entry['user_name']
            artist_full_path = art_entry['user_path']
            db.execute("""
            INSERT INTO public.artists (artist_name, follows, artist_full_path)
            VALUES ( '{}',{},'{}' )""".format(user_name, True, artist_full_path))
            db.commit()

    def db_get_artists(self):
        db = db_session()
        artist_list = db.execute("""
        SELECT artist_full_path FROM public.artists
        """)
        return artist_list

    def db_update_artist_info(self, art_dict):
        db = db_session()
        db.execute("""
        INSERT INTO public.artists (artist_active, artist_telegram, artist_twitter, updated_on)
        VALUES ( {}, '{}', '{}', {})
        WHERE artist_full_path = {}""".format(art_dict['active'],
                                              art_dict['telegram'],
                                              art_dict['twitter'],
                                              datetime.now(tz=False),
                                              art_dict['full_path']))
        db.commit()
