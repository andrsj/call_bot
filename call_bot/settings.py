from call_bot.setting.postgresql import *

SQL_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


try:
    from call_bot.setting.bot import *
except Exception as e:
    print(e)

