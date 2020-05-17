from discord.ext import commands

from settings import DISCORD_BOT_TOKEN
from models import Session, Phone, Base, engine


bot = commands.Bot(command_prefix='!')
session = None


@bot.event
async def on_ready():
    Base.metadata.create_all(engine)
    global session
    session = Session()
    print('Ready')


@bot.command(name='save')
async def save_phone(ctx, phone, name):
    phone = Phone(phone, name)
    session.add(phone)
    session.commit()
    await ctx.send(f'Add done -> {phone}')


@bot.command(name='pb')
async def list_phones(ctx):
    for phone in session.query(Phone).all():
        await ctx.send(phone)


@bot.command(name='clear')
async def clear_messages(ctx, amount: int = 1):
    await ctx.channel.purge(limit=amount)


@bot.command(name='exit')
async def exit_bot(ctx):
    await ctx.send('BB')
    exit('Close bot')

if __name__ == '__main__':
    bot.run(DISCORD_BOT_TOKEN)
