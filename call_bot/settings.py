# SQL_URL = 'sqlite:///callbot.db'
from configparser import ConfigParser
config = ConfigParser()
config.read('postgres.env')

POSTGRES_USER = config.get('POSTGRES', 'POSTGRES_USER')
POSTGRES_DB = config.get('POSTGRES', 'POSTGRES_DB')
POSTGRES_PASSWORD = config.get('POSTGRES', 'POSTGRES_PASSWORD')
POSTGRES_PORT = config.get('POSTGRES', 'POSTGRES_PORT')
POSTGRES_HOST = config.get('POSTGRES', 'POSTGRES_HOST')

SQL_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


try:
    from call_bot.local_settings import *
except Exception as e:
    print(e)

