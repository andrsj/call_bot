from discord.ext import commands


from call_bot.models import Base, engine
from call_bot.commands import PhoneBook


bot = commands.Bot(command_prefix='!')
bot.add_cog(PhoneBook(bot))


@bot.event
async def on_ready():
    Base.metadata.create_all(engine)
    print('Ready')
