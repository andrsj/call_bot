from discord.ext.commands import Cog
from discord.ext import commands


class NotForDeployCommandBot(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', brief='Clearing certain amount messages')
    async def clear_messages(self, ctx, amount: int = 1):
        await ctx.channel.purge(limit=amount)

    @commands.command(name='exit', brief='Switch off bot')
    async def exit_bot(self, ctx):
        await ctx.send('BB')
        await self.bot.close()
