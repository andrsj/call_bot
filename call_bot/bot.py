from discord.ext import commands


from call_bot.listeners import on_ready
from call_bot.commands import PhoneBook, NotForDeployCommandBot


def create_bot():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(PhoneBook(bot))
    bot.add_cog(NotForDeployCommandBot(bot))
    bot.add_listener(on_ready)

    return bot
