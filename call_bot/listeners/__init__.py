from discord.ext.commands import CommandNotFound


from call_bot.models import Base, engine


async def on_ready():
    Base.metadata.create_all(engine)
    print('Ready')


async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(error)
    else:
        print('Error: ', error)
        print('Args: ', error.args)
        print('Original: ', error.original)

