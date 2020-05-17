from call_bot.models import Base, engine


async def on_ready():
    Base.metadata.create_all(engine)
    print('Ready')
