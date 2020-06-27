from discord.ext.commands import Cog, Context
from discord.ext import commands
from discord import Embed
from textwrap import dedent

from call_bot.models import session, Phone
from call_bot.messages import ManagerMessages


description = {
    'save': dedent(
        """Saving phone number in phone book
        
        Attributes:
        Phone: string <required>
        Name: string <required>
        Priority: boolean [default => False]
        Banned: boolean [default => False]

        P.S. For True u can use:
        ['yes', 'y', 'true', 't', '1', 'enable', 'on']
        For False u can use:
        ['no', 'n', 'false', 'f', '0', 'disable', 'off']"""
    ),
    'pb':   "Display a list of all numbers in phone book",
    'edit': dedent(
        """Edit username by phone number in phone book
        
        Use the command to edit the name `edit name`
        Use the command to edit the phone number `edit number`"""
    ),
    'edit name': dedent(
        """Name editing command
        
        Attributes:
        Phone: string <required>
        New name: string <required>
        """
    ),
    'edit number': dedent(
        """Number editing command
        
        Attributes:
        Phone: string <required>
        New phone: string <required>        
        """
    ),
    'prior': dedent(
        """The command gives priority to the user by number
        If the user was not previously in the database, 
        the command will save the user along with the name
        
        Attributes:
        Phone: string <required>
        New name: string <required>
        """
    ),
    'ban': dedent(
        """Bans the user by phone number
        
        Attributes:
        Phone: string <required>
        """
    ),
    'priordel': dedent(
        """The command removes the priority 
        from the user who is searched by phone number
        
        Attributes:
        Phone: string <required>
        """
    ),
    'priorlist': "Display a list of all priority numbers in phone book",
    'unban': dedent(
        """I remove the ban from the user by number
        
        Attributes:
        Phone: string <required>
        """
    ),
    'banlist': "Display a list of all banned numbers in phone book",
    'deletephone': "Removes the user from the phonebook",

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

    @commands.command(name='save', help=description['save'], usage='')
    async def save_phone(self, ctx, number, name, priority: bool = False, banned: bool = False):
        """Saving phone numbers in phone book"""

        phone = Phone(number, name, priority, banned)
        if self._check_for_record_by_name(phone):
            await ctx.send(ManagerMessages.get_message_phone_already_exist('name', name))
        elif self._check_for_record_by_phonenumber(phone):
            await ctx.send(ManagerMessages.get_message_phone_already_exist('number', number))
        else:
            session.add(phone)
            session.commit()
            await ctx.send(ManagerMessages.get_message_succesfully_add_phone(phone))

    @commands.command(name='pb', help=description['pb'], usage='')
    async def list_phones(self, ctx):
        """Display a list of all numbers"""

        embed = Embed()
        embed.colour = 0xFF0000
        embed.title = 'List of alls numbers in phone book'

        text = '\n'.join(
            [
                ManagerMessages.phone_format(
                    phone.phone,
                    phone.name,
                    phone.priority,
                    phone.banned
                )
                for phone in session.query(Phone).order_by(Phone.name)
            ]
        )
        if text:
            embed.add_field(name='List <Name : Phone>', value='```' + text + '```')
        else:
            embed.add_field(name='Ooops, not found numbers', value='U need to add number into phone book')

        await ctx.send(embed=embed)

    @staticmethod
    def _work_with_prioritet_in_find_phone(phone: Phone):
        if phone.priority:
            return ManagerMessages.get_message_phone_already_in('priority')

        phone.priority = True
        session.commit()
        return ManagerMessages.get_message_succesfully_update_phone_prioritet(phone)

    def _prior_without_name(self, number):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number) \
            .first()

        if phone_by_number:
            result = self._work_with_prioritet_in_find_phone(phone_by_number)
            return result

        return ManagerMessages.get_message_not_found_number()

    def _prior_with_phone_model(self, name, number):
        phone_by_name_and_number = session.query(Phone) \
            .filter(Phone.name == name, Phone.phone == number) \
            .first()

        if phone_by_name_and_number:
            return self._work_with_prioritet_in_find_phone(phone_by_name_and_number)

        if self._check_for_record_by_phonenumber(number):
            return ManagerMessages.get_message_phone_already_exist_()
        elif self._check_for_record_by_name(name):
            return ManagerMessages.get_message_phone_already_exist_()
        else:
            phone = Phone(number, name, True, False)
            session.add(phone)
            session.commit()
            return ManagerMessages.get_message_succesfully_add_phone(phone)

    @commands.command(name='prior', aliases=['p'], help=description['prior'], usage='')
    async def prioritet(self, ctx, number, name=None):
        """
        Gives priority to the user

        Args:
            ctx: Context of discord message command
            number: Phone number user
            name: New user name

        """
        if name is None:
            result = self._prior_without_name(number)
            await ctx.send(result)

        else:
            result = self._prior_with_phone_model(name, number)
            await ctx.send(result)

    @staticmethod
    def _remove_prior_from_phone(number):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number) \
            .first()
        if not phone_by_number.priority:
            return ManagerMessages.get_message_phone_already_in('not priority')

        phone_by_number.priority = False
        session.commit()
        return ManagerMessages.get_message_succesfully_remove_prior_number(number)

    @commands.command(name='priordel', aliases=['pd'], help=description['priordel'], usage='')
    async def delete_prioritet(self, ctx: Context, number):
        """
        Remove prioritet from user

        Args:
            ctx: Context of discord message command
            number: Phone number user

        """
        if self._check_for_record_by_phonenumber(number):
            await ctx.send(self._remove_prior_from_phone(number))
        else:
            await ctx.send(ManagerMessages.get_message_not_found_phone(number))

    @commands.command(name='priorlist', aliases=['pl'], help=description['priorlist'], usage='')
    async def list_priority_phones(self, ctx: Context):
        """Display a list of all priority numbers in phone book"""

        embed = Embed()
        embed.colour = 0x00FF00
        embed.title = 'List of priority numbers in phone book'

        text = '\n'.join(
            [
                ManagerMessages.phone_format(
                    phone.phone,
                    phone.name,
                    phone.priority,
                    phone.banned
                )
                for phone in session.query(Phone).filter(Phone.priority).order_by(Phone.name)
            ]
        )
        if text:
            embed.add_field(name='List <Name : Phone>', value='```' + text + '```')
        else:
            embed.add_field(name='Ooops, not found numbers', value='Phone book does have numbers with priority')

        await ctx.send(embed=embed)

    @staticmethod
    def _give_ban_for_number(number):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number) \
            .first()

        if phone_by_number.banned:
            return ManagerMessages.get_message_phone_already_in('ban')

        phone_by_number.banned = True
        session.commit()
        return ManagerMessages.get_message_succesfully_ban_number(number)

    @commands.command(name='ban', aliases=['b'], help=description['ban'], usage='')
    async def give_ban(self, ctx: Context, number):
        """
        Bans the user by phone number

        Args:
            ctx: Context of discord message command
            number: Phone number user

        """
        if self._check_for_record_by_phonenumber(number):
            await ctx.send(self._give_ban_for_number(number))
        else:
            await ctx.send(ManagerMessages.get_message_not_found_phone(number))

    @staticmethod
    def _remove_ban_for_number(number):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number) \
            .first()

        if not phone_by_number.banned:
            return ManagerMessages.get_message_phone_already_in('unban')

        phone_by_number.banned = False
        session.commit()
        return ManagerMessages.get_message_succesfully_remove_ban_number(number)

    @commands.command(name='unban', aliases=['ub'], help=description['unban'], usage='')
    async def unban(self, ctx: Context, number):
        """
        Removes the ban from the user

        Args:
            ctx: Context of discord message command
            number: Phone number user

        """
        if self._check_for_record_by_phonenumber(number):
            await ctx.send(self._remove_ban_for_number(number))
        else:
            await ctx.send(ManagerMessages.get_message_not_found_phone(number))

    @commands.command(name='banlist', aliases=['bl'], help=description['banlist'], usage='')
    async def list_banned_phones(self, ctx: Context):
        """Display a list of all banned numbers in phone book"""

        embed = Embed()
        embed.colour = 0x00FF00
        embed.title = 'List of banned numbers in phone book'

        text = '\n'.join(
            [
                ManagerMessages.phone_format(
                    phone.phone,
                    phone.name,
                    phone.priority,
                    phone.banned
                )
                for phone in session.query(Phone).filter(Phone.banned).order_by(Phone.name)
            ]
        )

        if text:
            embed.add_field(name='List <Name : Phone>', value='```' + text + '```')
        else:
            embed.add_field(name='Ooops, not found numbers', value='Phone book does have numbers with ban')

        await ctx.send(embed=embed)

    @staticmethod
    def _delete_number(number):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number)
        phone_by_number.delete()
        session.commit()
        return ManagerMessages.get_message_succesfully_delete_phone(number)

    @commands.command(name='deletephone', aliases=['dp', 'delphone', 'delph'], usage='')
    async def delete_phone(self, ctx: Context, number):
        """Removes the user from the phonebook"""

        if self._check_for_record_by_phonenumber(number):
            await ctx.send(self._delete_number(number))
        else:
            await ctx.send(ManagerMessages.get_message_not_found_phone(number))

    @staticmethod
    def _edit_name(number, new_name):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number) \
            .first()
        phone_by_number.name = new_name
        session.commit()
        return ManagerMessages.get_message_succesfully_update_phone(number, 'Name', new_name)

    @staticmethod
    def _edit_number(number, new_number):
        phone_by_number = session.query(Phone) \
            .filter(Phone.phone == number) \
            .first()
        phone_by_number.phone = new_number
        session.commit()
        return ManagerMessages.get_message_succesfully_update_phone(number, 'Phone', new_number)

    @commands.group(name='edit', aliases=['e'], help=description['edit'], usage='')
    async def base_edit(self, ctx: Context):
        """Edit user command"""

        if ctx.invoked_subcommand is None:
            await ctx.send(ManagerMessages.get_message_help_edit())

    @base_edit.command(name='number', aliases=['num'], help=description['edit number'], usage='')
    async def edit_number(self, ctx: Context, number, new_value):
        """
        Number editing command

        Args:
            ctx: Context of discord message command
            number: Phone number user
            new_value: New number user
        """

        if self._check_for_record_by_phonenumber(number):
            await ctx.send(self._edit_number(number, new_value))
        else:
            await ctx.send(ManagerMessages.get_message_not_found_phone(number))

    @base_edit.command(name='name', help=description['edit name'], usage='')
    async def edit_name(self, ctx: Context, number, new_value):
        """
        Name editing command

        Args:
            ctx: Context of discord message command
            number: Phone number user
            new_value: New name user

        """
        if self._check_for_record_by_phonenumber(number):
            await ctx.send(self._edit_name(number, new_value))
        else:
            await ctx.send(ManagerMessages.get_message_not_found_phone(number))
