from discord.ext import commands


from call_bot.listeners import on_ready, on_command_error
from call_bot.commands import PhoneBook, NotForDeployCommandBot, Configuration


def create_bot():
    bot = commands.Bot(command_prefix='')
    bot.add_cog(PhoneBook(bot))
    bot.add_cog(NotForDeployCommandBot(bot))
    bot.add_cog(Configuration(bot))
    bot.add_listener(on_ready)
    bot.add_listener(on_command_error)

    return bot
