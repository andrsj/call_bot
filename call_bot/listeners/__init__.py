from discord.ext.commands import CommandNotFound, MissingRequiredArgument


from call_bot.models import Base, engine


async def on_ready():
    Base.metadata.create_all(engine)


async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(error)
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send(f'U miss required parametr \'{error.param}\'')
    else:
        print(error)
        await ctx.send(error)
