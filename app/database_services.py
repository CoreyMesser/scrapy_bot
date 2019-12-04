from datetime import datetime
import pandas as pd
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

    def db_update_artist_info(self, user_dict):
        updated_on = datetime.now()
        db = db_session()
        db.execute("""
        UPDATE public.artists 
        SET artist_active = {}, 
        artist_telegram = '{}', 
        artist_twitter = '{}', 
        updated_on = now()
        WHERE artist_full_path = '{}'
        """.format(user_dict['active'],
                   user_dict['telegram'],
                   user_dict['twitter'],
                   user_dict['full_path']))
        db.commit()

    def get_twitter_list(self):
        db = db_session()
        sql = """
        SELECT artists from public.artists where artists not like 'None'
        """
        return db.execute(sql)

    def df_to_csv(self, data):
        df = pd.DataFrame(data)
        df.to_csv()


    def get_telegram_list(self):
        pass