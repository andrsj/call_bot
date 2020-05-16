from discord.ext import commands
from .settings import DISCORD_BOT_TOKEN

bot = commands.Bot(command_prefix='!')


@bot.command(name='call')
async def nine_nine(ctx):
    response = "Not ready yet. But glad to see that someone checking my english"
    await ctx.send(response)


bot.run(DISCORD_BOT_TOKEN)
