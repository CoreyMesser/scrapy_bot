from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgres://localhost/rndrols")
db_session = sessionmaker(bind=engine)
