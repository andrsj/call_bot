from discord.ext.commands import Cog
from discord.ext import commands
from discord import Embed

from call_bot.models import session, Phone


brief = {
    'save': 'Saving phone numbers in phone book',
    'pb': 'Display a list of all numbers',
    'edit': 'Editing saved phone number names',
}

description = {
    'save': 'Saving phone number in phone book\n'
            'Attributes:\n'
            'Phone: string <required>\n'
            'Name: string <required>\n'
            'Priority: boolean [default => False]\n'
            'Banned: boolean [default => False]\n'
            '\n'
            'P.S. For True u can use:\n'
            "['yes', 'y', 'true', 't', '1', 'enable', 'on']\n"
            'For False u can use:\n'
            "['no', 'n', 'false', 'f', '0', 'disable', 'off']",
    'pb':   'Display a list of all numbers',
    'edit': 'Edit username by phone number in phone book\n'
            'Attributes:\n'
            'Phone: string <required>\n'
            'New name: string <required>',
}


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

    @commands.command(name='save', brief=brief['save'], description=description['save'])
    async def save_phone(self, ctx, phone, name, priority: bool = False, banned: bool = False):

        phone = Phone(phone, name, priority, banned)
        if self._check_for_record_by_name(phone):
            await ctx.send(f'User with this phone number \'{phone.phone}\'\n'
                           f'{phone} is already exist\n'
                           'U can use !edit command for change name')
        elif self._check_for_record_by_phonenumber(phone):
            await ctx.send(f'User with this name \'{phone.name}\'\n'
                           f'{phone} is already exist\n'
                           'U can use !pb command for searching in phone book')
        else:
            session.add(phone)
            session.commit()
            await ctx.send(f'Add done: {phone}')

    @save_phone.error
    async def save_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'U miss required parametr \'{error.param}\'\n'
                           f'Syntaxis: `!save phone_number user_name priority: bool, banned: bool`')

    @commands.command(name='edit', brief=brief['edit'], description=description['edit'])
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

    @commands.command(name='pb', brief=brief['pb'], description=description['pb'])
    async def list_phones(self, ctx):
        embed = Embed()
        embed.colour = 0xFF0000
        embed.title = 'List of alls phone-numbers in phonebook'

        # Formating like '<1000' dosn`t work in Embed
        # Embed eat all spaces more one
        text = '\n'.join([f'{phone.name} : {phone.phone}' for phone in session.query(Phone).all()])
        if text:
            embed.add_field(name='List <Name : Phone>', value=text)
            await ctx.send(embed=embed)
        else:
            embed.add_field(name='Ooops, not found numbers', value='U need to add number into phone book')
            await ctx.send(ember=embed)
