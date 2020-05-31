from discord.ext.commands import Cog
from discord.ext import commands


from call_bot.setting.botConfig import config


class NotForDeployCommandBot(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', brief='Clearing certain amount messages')
    async def clear_messages(self, ctx, amount: int = 1):
        await ctx.channel.purge(limit=amount)

    @commands.command(name='exit', brief='Switch off bot')
    async def exit_bot(self, ctx):
        await ctx.send('BB')
        exit('Close bot')

    @commands.command(name='aa_sec')
    async def get_aa_sec(self, ctx):
        await ctx.send(f"'aa[sec]' = {config.get('conf', 'aa_sec')}")

    @commands.command(name='autotake_sec')
    async def get_autotake_sec(self, ctx):
        await ctx.send(f"'autotake[sec]' = {config.get('conf', 'autotake_sec')}")
