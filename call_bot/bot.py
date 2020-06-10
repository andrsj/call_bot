from discord.ext import commands
from discord import Message
from discord.ext.commands import Context

from call_bot.listeners import Listeners
from call_bot.commands import PhoneBook, NotForDeployCommandBot, Configuration


def create_bot():
    bot = commands.Bot(command_prefix='')
    bot.add_cog(PhoneBook(bot))
    bot.add_cog(NotForDeployCommandBot(bot))
    bot.add_cog(Configuration(bot))
    bot.add_cog(Listeners(bot))

    @bot.event
    async def on_message(message: Message):
        """
        This function check author of message
        At first we check if context message raise a command
        After check author is bot user or not if message not raise command
        Else command will be raised all time (from bot or not)
        """
        ctx: Context = await bot.get_context(message)
        if ctx.command is not None:
            await bot.invoke(ctx)
        else:
            if ctx.author.bot:
                return
            else:
                await bot.process_commands(message)

    return bot
