from app.models import FaScrape, Artist
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from app.constants import EnvConstants as ec
from datetime import datetime


class DBConnection(object):

    engine = create_engine("postgres://localhost/rndrols")
    if not database_exists(engine.url):
        create_database(engine.url)

    print(database_exists(engine.url))
    conn = engine.connect()
    db_session = sessionmaker(bind=engine)




class DBServices(DBConnection):

    def db_update_artists_names(self, names_dict):
        db = DBConnection().db_session()
        art = Artist()
        for art_entry in names_dict:
            art.artist_name = art_entry['user_name']
            art.follows = True
            art.artist_full_path = ec.TARGET_SITE + '/' + ec.PATH_USER + art_entry['user_path']
            art.created_on = datetime.now()
            db.add(art)
            db.commit()

