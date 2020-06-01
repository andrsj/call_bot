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
    def _check_for_record_by_name(item):
        if isinstance(item, Phone):
            return bool(
                session.query(Phone)
                .filter(Phone.name == item.name)
                .first()
            )
        elif isinstance(item, str):
            return bool(
                session.query(Phone)
                .filter(Phone.name == item)
                .first()
            )
        else:
            raise TypeError(f'{type(item)} is not Phone or str')

    @staticmethod
    def _check_for_record_by_phonenumber(item):
        if isinstance(item, Phone):
            return bool(
                session.query(Phone)
                .filter(Phone.phone == item.name)
                .first()
            )
        elif isinstance(item, str):
            return bool(
                session.query(Phone)
                .filter(Phone.phone == item)
                .first()
            )
        else:
            raise TypeError(f'{type(item)} is not Phone or str')

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

    @commands.command(name='edit', brief=brief['edit'], description=description['edit'])
    async def edit_name_by_phone(self, ctx, phone, new_name):
        phone_by_name = session.query(Phone) \
            .filter(Phone.phone == phone) \
            .first()
        if phone_by_name:
            phone_by_name.name = new_name
            session.commit()
            await ctx.send(f'Phone: {phone_by_name} succesfully updated')
        else:
            await ctx.send(f'User by \'{phone}\' not found!')

    @commands.command(name='pb', brief=brief['pb'], description=description['pb'])
    async def list_phones(self, ctx):
        embed = Embed()
        embed.colour = 0xFF0000
        embed.title = 'List of alls phone-numbers in phonebook'

        # Formating like '<1000' dosn`t work in Embed
        # Embed eat all spaces more one
        text = '\n'.join(
            sorted([f'{phone.name} : {phone.phone} '
                    f'[p:{phone.priority} b:{phone.banned}]'
                    for phone in session.query(Phone).all()])
        )
        if text:
            embed.add_field(name='List <Name : Phone>', value=text)
            await ctx.send(embed=embed)
        else:
            embed.add_field(name='Ooops, not found numbers', value='U need to add number into phone book')
            await ctx.send(embed=embed)

    @staticmethod
    def _work_with_find_phone(phone: Phone):
        if phone.priority:
            return 'This number already in prioritet'
        else:
            phone.priority = True
            session.commit()
            return f'{phone} succesfully updated priority to \'True\''

    def _prior_without_name(self, number):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number) \
            .first()
        if phone_by_number:
            result = self._work_with_find_phone(phone_by_number)
            return result
        else:
            return 'This phone number not found in phone book\n' \
                   'Check in \'pb\' for searching'

    def _prior_with_phone_model(self, name, number):
        phone_by_name_and_number = session.query(Phone) \
            .filter(Phone.name == name, Phone.phone == number) \
            .first()

        if phone_by_name_and_number:
            return self._work_with_find_phone(phone_by_name_and_number)

        else:
            if self._check_for_record_by_phonenumber(number):
                return 'This phone number already exist\n' \
                       'Check in \'pb\' for searching'
            elif self._check_for_record_by_name(name):
                return 'This user already exist in phone book\n' \
                       'Check in \'pb\' for searching'
            else:
                phone = Phone(number, name, True, False)
                session.add(phone)
                session.commit()
                return f'{phone} succesfully add to phone book with priority \'True\''

    @commands.command(name='prior', aliases=['p'])
    async def prioritet(self, ctx, number, name=None):
        if name is None:
            result = self._prior_without_name(number)
            await ctx.send(result)

        else:
            result = self._prior_with_phone_model(name, number)
            await ctx.send(result)
