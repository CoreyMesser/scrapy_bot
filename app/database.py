from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql:///postgres")
db_session = sessionmaker(bind=engine)
