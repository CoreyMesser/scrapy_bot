from sqlalchemy import Column, Integer, Text, text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, server_default=text("nextval('artists_id_seq'::regclass)"))
    artist_id = Column(Integer)
    artist_name = Column(Text)
    follows = Column(Boolean)
    artist_full_path = Column(Text)
    artist_twitter = Column(Text)
    artist_telegram = Column(Text)
    artist_active = Column(Boolean)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime)


class FaScrape(Base):
    __tablename__ = 'fa_scrape'

    id = Column(Integer, primary_key=True, server_default=text("nextval('fa_scrape_id_seq'::regclass)"))
    cf_token = Column(Text)
    current_watchers = Column(Integer)
    previous_watcher = Column(Integer)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime)
