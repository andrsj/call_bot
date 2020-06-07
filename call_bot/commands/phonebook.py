from discord.ext.commands import Cog
from discord.ext import commands
from discord import Embed

from call_bot.models import session, Phone
from call_bot.messages import ManagerMessages


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
                .filter(Phone.phone == item.phone)
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
    async def save_phone(self, ctx, number, name, priority: bool = False, banned: bool = False):

        phone = Phone(number, name, priority, banned)
        if self._check_for_record_by_name(phone):
            await ctx.send(ManagerMessages.get_message_phone_already_exist('name', name))
        elif self._check_for_record_by_phonenumber(phone):
            await ctx.send(ManagerMessages.get_message_phone_already_exist('number', number))
        else:
            session.add(phone)
            session.commit()
            await ctx.send(ManagerMessages.get_message_succesfully_add_phone(phone))

    @commands.command(name='edit', brief=brief['edit'], description=description['edit'])
    async def edit_name_by_phone(self, ctx, phone, new_name):
        phone_by_name = session.query(Phone) \
            .filter(Phone.phone == phone) \
            .first()
        if phone_by_name:
            phone_by_name.name = new_name
            session.commit()
            await ctx.send(ManagerMessages.get_message_succesfully_update_phone(phone_by_name))
        else:
            await ctx.send(ManagerMessages.get_message_not_found_phone(phone))

    @commands.command(name='pb', brief=brief['pb'], description=description['pb'])
    async def list_phones(self, ctx):
        embed = Embed()
        embed.colour = 0xFF0000
        embed.title = 'List of alls phone-numbers in phonebook'

        # Formating like '<1000' dosn`t work in Embed
        # Embed eat all spaces more one
        text = '\n'.join(
            [f'{phone.name} : {phone.phone} '
             f'[p:{phone.priority} b:{phone.banned}]'
             for phone in session.query(Phone).order_by(Phone.name)]
        )
        if text:
            embed.add_field(name='List <Name : Phone>', value='```' + text + '```')
            await ctx.send(embed=embed)
        else:
            embed.add_field(name='Ooops, not found numbers', value='U need to add number into phone book')
            await ctx.send(embed=embed)

    @staticmethod
    def _work_with_find_phone(phone: Phone):
        if phone.priority:
            return ManagerMessages.get_message_phone_already_in_prioritet()
        else:
            phone.priority = True
            session.commit()
            return ManagerMessages.get_message_succesfully_update_phone_prioritet(phone)

    def _prior_without_name(self, number):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number) \
            .first()
        if phone_by_number:
            result = self._work_with_find_phone(phone_by_number)
            return result
        else:
            return ManagerMessages.get_message_not_found_number()

    def _prior_with_phone_model(self, name, number):
        phone_by_name_and_number = session.query(Phone) \
            .filter(Phone.name == name, Phone.phone == number) \
            .first()

        if phone_by_name_and_number:
            return self._work_with_find_phone(phone_by_name_and_number)
        else:
            if self._check_for_record_by_phonenumber(number):
                return ManagerMessages.get_message_phone_already_exist_()
            elif self._check_for_record_by_name(name):
                return ManagerMessages.get_message_phone_already_exist_()
            else:
                phone = Phone(number, name, True, False)
                session.add(phone)
                session.commit()
                return ManagerMessages.get_message_succesfully_add_phone(phone)

    @commands.command(name='prior', aliases=['p'])
    async def prioritet(self, ctx, number, name=None):
        if name is None:
            result = self._prior_without_name(number)
            await ctx.send(result)

        else:
            result = self._prior_with_phone_model(name, number)
            await ctx.send(result)
