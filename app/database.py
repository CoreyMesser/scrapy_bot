from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.constants import EnvConstants

engine = create_engine(f"postgresql:///{EnvConstants.DATABASE}")
db_session = sessionmaker(bind=engine)
