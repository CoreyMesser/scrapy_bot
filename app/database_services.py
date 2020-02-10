from datetime import datetime
import pandas as pd
from app.database import db_session
from app.aws_services import AWSServices

from app.logger import LoggerService

ls = LoggerService()
_log = ls.get_logger()


class DBServices(object):

    def parse_resultsproxy_to_dict(self, result):
        d, a = {}, []
        for rowproxy in result:
            for column, value in rowproxy.items():
                d = {**d, **{column: value}}
            a.append(d)
        return a

    def db_add_artists_names(self, names_dict):
        db = db_session()
        for art_entry in names_dict:
            user_name = art_entry['user_name']
            artist_full_path = art_entry['user_path']
            db.execute("""
            INSERT INTO public.artists (artist_name, follows, artist_full_path)
            VALUES ( '{}',{},'{}' )""".format(user_name, True, artist_full_path))
            db.commit()

    def db_get_artist(self, user):
        db = db_session()
        results = db.execute("""
            SELECT * FROM public.artists WHERE artist_full_path = '{}'
            """.format(user))
        return results

    def db_get_artists(self):
        db = db_session()
        results =  db.execute("""
            SELECT artist_full_path FROM public.artists
            """)
        return results

    def db_update_artist_unfollow(self, user):
        db = db_session()
        db.execute("""
                UPDATE public.artists 
                SET follows = False, updated_on = now()
                WHERE artist_full_path = '{}'
                """.format(user))
        db.commit()

    def db_update_artist_follow(self, user):
        db = db_session()
        db.execute("""
                UPDATE public.artists 
                SET follows = True, updated_on = now()
                WHERE artist_full_path = '{}' 
                """.format(user))
        db.commit()

    def db_get_artists_social_update(self):
        db = db_session()
        artist_list = db.execute("""
        SELECT artist_full_path FROM public.artists ar where ar.artist_twitter is null
        """)
        return artist_list

    def get_twitter_list(self):
        db = db_session()
        sql = """
        SELECT artist_twitter from public.artists where artist_twitter not like 'None'
        """
        return db.execute(sql)

    def df_to_csv_to_s3(self, data):
        awss = AWSServices()
        path = awss.assemble_s3_path_twitter()
        df = pd.DataFrame(data)
        return df.to_csv()

    def get_telegram_list(self):
        pass

    def db_get_followers(self):
        db = db_session()
        artist_list = db.execute("""
        SELECT artist_full_path FROM public.artists WHERE follows = True
        """)
        return artist_list

    def db_get_unfollowers(self):
        db = db_session()

    def get_new_artists(self, current_list):
        db_list = self.db_get_followers()
        cl_df = pd.DataFrame(current_list)
        dl_df = pd.DataFrame(db_list)
        _log.info("Getting New Artists")
        results = set(cl_df['user_path']).difference(set(dl_df[0]))
        return results

    def get_artist_integrity(self, current_list):
        db_list = self.db_get_followers()
        cl_df = pd.DataFrame(current_list)
        dl_df = pd.DataFrame(db_list)
        resultalt = set(dl_df[0]).difference(set(cl_df['user_path']))
        if len(resultalt) > 0:
            for user in list(resultalt):
                _log.info('I see... {} unfollowed'.format(user))
                self.db_update_artist_unfollow(user=user)

    def db_artist_check(self, watch_dict):
        new_artists_list = []
        _log.info('Checking Artist against Database')
        new_artists = self.get_new_artists(current_list=watch_dict)
        for artist in new_artists:
            artist_exists = self.db_get_artist(user=artist)
            if artist_exists.rowcount == 1:
                _log.info('Looks like an unfollower followed again...')
                artist_dict = self.parse_resultsproxy_to_dict(result=artist_exists)
                if not artist_dict[0]['follows']:
                    _log.info('WELL WELL WELL LOOK WHO COMES CRAWLING BACK {}'.format(artist_dict[0]['artist_name']))
                    self.db_update_artist_follow(user=artist)
            elif artist_exists.rowcount == 0:
                new_artists_list.append(artist)
        return new_artists_list

    def db_update_artist_info(self, user_dict):
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
