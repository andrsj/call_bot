from discord.ext.commands import Cog
from discord.ext import commands

from call_bot.models import session, Phone


class PhoneBook(Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def _check_for_record_by_name(model):
        return bool(
            session.query(Phone)
                .filter(Phone.phone == model.phone)
                .first()
        )

    @staticmethod
    def _check_for_record_by_phonenumber(model):
        return bool(
            session.query(Phone)
                .filter(Phone.phone == model.phone)
                .first()
        )

    @commands.command(name='save')
    async def save_phone(self, ctx, phone, name):

        phone = Phone(phone, name)
        if self._check_for_record_by_name(phone):
            await ctx.send(f'User with this phone number \'{phone.phone}\'\n'
                           f'{phone} is already exist\n'
                           'U can use !edit command for change name')
        elif self._check_for_record_by_phonenumber(phone):
            await ctx.send(f'User with this name \'{phone.name}\'\n'
                           f'{phone} is already exist\n'
                           'U can use !pb command for searching in phonebook')
        else:
            session.add(phone)
            session.commit()
            await ctx.send(f'Add done -> {phone}')

    @commands.command(name='edit')
    async def edit_name_by_phone(self, ctx, phone, new_name):
        phone_by_name = session.query(Phone) \
            .filter(Phone.phone == phone) \
            .first()
        if phone_by_name:
            phone_by_name.name = new_name
            session.commit()
            await ctx.send(f'Phone {phone_by_name} succesfully updated')
        else:
            await ctx.send(f'User by \'{phone}\' not found!')

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
