from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from call_bot.settings import SQL_URL

Base = declarative_base()
engine = create_engine(SQL_URL, echo=True)
