from datetime import datetime
import pandas as pd
from app.database import db_session
from app.aws_services import AWSServices

from app.logger import LoggerService
from constants import EnvConstants as ec

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

    def db_add_artists_names(self, names_dict, watch):
        db = db_session()
        heart_beat_counter = 0
        db_tools = self.db_watch_toolbox(watch=watch)
        for art_entry in names_dict:
            user_name = art_entry['user_name']
            artist_full_path = art_entry['user_path']
            db.execute(f"""
            INSERT INTO {db_tools['table']} (artist_name, {db_tools['follows']}, artist_full_path)
            VALUES ( '{user_name}',{True},'{artist_full_path}' )""")
            db.commit()
            heart_beat_counter += 1
            heartbeat = (heart_beat_counter / 100) % 2
            if heartbeat == 0 or heartbeat == 1:
                _log.info(f"[DATABASE][HEARBEAT] {heart_beat_counter} added!")
        _log.info(f"[DATABASE] {heart_beat_counter} artists added!!")

    def db_get_artist(self, user, watch):
        db = db_session()
        results = db.execute(f"""
            SELECT * FROM {watch['table']} WHERE artist_full_path = '{user['user_path']}'
            """)
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

    def db_update_artist_follow(self, user, watch):
        db = db_session()
        db.execute(f"""
                UPDATE {watch['table']} 
                SET {watch['follows']} = True, updated_on = now()
                WHERE artist_full_path = '{user}' 
                """)
        db.commit()

    def db_get_artists_social_update(self, watch):
        db_tools = self.db_watch_toolbox(watch=watch)
        db = db_session()
        return db.execute(f"""
        SELECT artist_full_path FROM {db_tools['table']} where artist_twitter is null
        """)

    def get_twitter_list(self):
        db = db_session()
        return db.execute("""
        SELECT artist_twitter from public.artists where artist_twitter not like 'None'
        """)

    def df_to_csv_to_s3(self, data):
        awss = AWSServices()
        path = awss.assemble_s3_path_twitter()
        df = pd.DataFrame(data)
        return df.to_csv()

    def get_telegram_list(self):
        pass

    def db_get_followers(self, watch):
        """
        returns artists following me or i am following
        :param watch:
        :return:
        """
        db = db_session()
        artist_list = db.execute(f"""
        SELECT artist_name, artist_full_path FROM {watch['table']} WHERE {watch['follows']} = True
        """)
        return artist_list

    def db_get_artists_i_unfollowed(self):
        pass

    def db_get_unfollowers(self):
        db = db_session()

    def db_i_follow_follow_me(self):
        db = db_session()
        i_follow = db.execute("""
        SELECT * FROM watched_artists WHERE follows_me = FALSE""")
        follows = db.execute("""
        SELECT * FROM artists WHERE follows = TRUE""")
        if_df = pd.DataFrame(i_follow)
        f_df = pd.DataFrame(follows)
        results = set(if_df[5]).intersection(set(f_df[3]))
        return results

    def db_set_follow_me(self, results):
        db = db_session()
        if len(results) > 0:
            for user in list(results):
                _log.info(f"[FOLLOW HARMONY] {user} follows me back!")
                user = str(user)
                db.execute(f"""
                UPDATE watched_artists
                SET follows_me = TRUE, follows_me_id = (SELECT id FROM artists WHERE artist_full_path = '{user}'), updated_on = now()
                WHERE artist_full_path = '{user}'""")
                _log.info(f"[FOLLOW HARMONY] {user} updated!")
                db.commit()
        else:
            _log.info("[FOLLOW HARMONY] No new follow backs.")


    def get_new_artists(self, current_list, watch):
        """
        takes a current list of users and compares them with an active list of users from the db
        :param current_list:
        :param watch:
        :return:
        """
        db_list = self.db_get_followers(watch=watch)
        cl_df = pd.DataFrame(current_list)
        dl_df = pd.DataFrame(db_list)
        first_time = False
        if len(dl_df) <= 0:
            _log.info("First time eh?")
            first_time = True
            return current_list, first_time
        else:
            _log.info("Getting New Artists")
            user_path = set(cl_df['user_path']).difference(set(dl_df[1]))
            user_name = set(cl_df['user_name']).difference(set(dl_df[0]))
            results = []
            for name in user_name:
                nl = name.lower()
                for path in user_path:
                    ps = path.split('/')[-2]
                    if nl == ps:
                        results.append({'user_name': name, 'user_path': path})
        return results, first_time

    def get_artist_integrity(self, current_list, watch):
        db_tools = self.db_watch_toolbox(watch=watch)
        db_list = self.db_get_followers(watch=db_tools)
        cl_df = pd.DataFrame(current_list)
        dl_df = pd.DataFrame(db_list)
        resultalt = set(dl_df[0]).difference(set(cl_df['user_path']))
        if len(resultalt) > 0:
            for user in list(resultalt):
                _log.info('I see... {} unfollowed'.format(user))
                self.db_update_artist_unfollow(user=user)

    def db_artist_check(self, watch_dict, watch):
        new_artists_list = []
        db_tools = self.db_watch_toolbox(watch=watch)
        _log.info('Checking Artist against Database')
        new_artists, first_time = self.get_new_artists(current_list=watch_dict, watch=db_tools)
        if not first_time:
            for artist in new_artists:
                artist_exists = self.db_get_artist(user=artist, watch=db_tools)
                if artist_exists.rowcount == 1:
                    _log.info('Looks like an unfollower followed again...')
                    artist_dict = self.parse_resultsproxy_to_dict(result=artist_exists)
                    if not artist_dict[0]['follows']:
                        _log.info('WELL WELL WELL LOOK WHO COMES CRAWLING BACK {}'.format(artist_dict[0]['artist_name']))
                        self.db_update_artist_follow(user=artist, watch=db_tools)
                elif artist_exists.rowcount == 0:
                    new_artists_list.append(artist)
        else:
            new_artists_list = new_artists
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

    def db_update_watching_info(self, user_dict, user_stats):
        db = db_session()
        db.execute(f"""
           UPDATE watched_artists 
           SET artist_active = {user_dict['active']}, 
           artist_telegram = '{user_dict['telegram']}', 
           artist_twitter = '{user_dict['twitter']}',
           watchers = {user_stats['watchers']},
           watching = {user_stats['watching']},
           views = {user_stats['views']},
           faves = {user_stats['faves']}, 
           updated_on = now()
           WHERE artist_full_path = '{user_dict['full_path']}'
           """)
        db.commit()

    def db_update_stats(self, stats_dict):
        db = db_session()
        prev_watchers = db.execute("""
        SELECT current_watchers from profile_stats where id = (select MAX(id) from profile_stats)""")
        db.execute("""INSERT INTO profile_stats (current_watchers, previous_watchers, watching, views, faves, updated_on, created_on)
        VALUES ( {}, {}, {}, {}, {}, now(), now())""".format(stats_dict['watchers'],
                                                             prev_watchers.fetchone()['current_watchers'],
                                                             stats_dict['watching'],
                                                             stats_dict['views'],
                                                             stats_dict['faves']))
        db.commit()

    def db_watch_toolbox(self, watch):
        db_dict = {}
        if watch == ec.PATH_WATCHLIST:
            db_dict = {'table': 'artists',
                       'follows': 'follows'}
        else:
            db_dict = {'table': 'watched_artists',
                       'follows': 'i_follow'}
        return db_dict
