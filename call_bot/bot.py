from discord.ext import commands


from call_bot.listeners import Listeners
from call_bot.commands import PhoneBook, NotForDeployCommandBot, Configuration


def create_bot():
    bot = commands.Bot(command_prefix='')
    bot.add_cog(PhoneBook(bot))
    bot.add_cog(NotForDeployCommandBot(bot))
    bot.add_cog(Configuration(bot))
    bot.add_cog(Listeners(bot))

    @bot.event
    async def on_message(message):
        ctx = await bot.get_context(message)
        if ctx.command is not None:
            await bot.invoke(ctx)
        else:
            if ctx.author.bot:
                return
            else:
                await bot.process_commands(message)

    return bot
