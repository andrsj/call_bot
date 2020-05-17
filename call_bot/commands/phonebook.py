from discord.ext.commands import Cog
from discord.ext import commands


from call_bot.models import session, Phone


class PhoneBook(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='save')
    async def save_phone(self, ctx, phone, name):
        phone = Phone(phone, name)
        session.add(phone)
        session.commit()
        await ctx.send(f'Add done -> {phone}')

    @commands.command(name='edit')
    async def edit_name_by_phone(self, ctx, phone, new_name):
        phone_by_name = session.query(Phone) \
            .filter(Phone.phone == phone) \
            .first()
        phone_by_name.name = new_name
        session.commit()
        await ctx.send(f'Phone {phone_by_name} succesfully updated')

    @commands.command(name='pb')
    async def list_phones(self, ctx):
        for phone in session.query(Phone).all():
            await ctx.send(phone)

    @commands.command(name='clear')
    async def clear_messages(self, ctx, amount: int = 1):
        await ctx.channel.purge(limit=amount)

    @commands.command(name='exit')
    async def exit_bot(self, ctx):
        await ctx.send('BB')
        exit('Close bot')
