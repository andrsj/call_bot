from discord.ext import commands


from call_bot.listeners import Listeners
from call_bot.commands import PhoneBook, NotForDeployCommandBot, Configuration


def create_bot():
    bot = commands.Bot(command_prefix='')
    bot.add_cog(PhoneBook(bot))
    bot.add_cog(NotForDeployCommandBot(bot))
    bot.add_cog(Configuration(bot))
    bot.add_cog(Listeners(bot))

    return bot
