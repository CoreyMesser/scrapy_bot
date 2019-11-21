from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgres://localhost/rndrols")
db_session = sessionmaker(bind=engine)