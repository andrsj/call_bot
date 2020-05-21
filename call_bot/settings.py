from call_bot.settings.postgresql import *

SQL_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


try:
    from call_bot.settings.bot import *
except Exception as e:
    print(e)

