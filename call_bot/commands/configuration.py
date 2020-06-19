from discord.ext.commands import Cog, Context
from discord.ext import commands
from typing import Union


from call_bot.setting.botConfig import config_bot as config
from call_bot.messages import ManagerMessages


class Bool:
    BOOLEAN_TRUE = ('on', )
    BOOLEAN_FALSE = ('off', )

    bool_value: bool
    str_value: str

    def __init__(self, value: Union[str, bool]):
        if isinstance(value, bool):
            self.bool_value = value
            self.str_value = self.BOOLEAN_TRUE[0] if value else self.BOOLEAN_FALSE[0]  # set first string from const str
        elif isinstance(value, str):
            if value in self.BOOLEAN_FALSE + self.BOOLEAN_TRUE:  # check if str_value in const tuple strings
                self.str_value = value
                self.bool_value = value in self.BOOLEAN_TRUE  # True if str_value in ['on', ...]
            else:
                raise ValueError(f'Invalid argument value: use [\'{self.BOOLEAN_TRUE}\', \'{self.BOOLEAN_FALSE}\']')
        else:
            raise TypeError('Value is not bool or str')

    def __bool__(self):
        return self.bool_value

    def __str__(self):
        return self.str_value


class Configuration(Cog):
    def __int__(self, bot):
        self.bot = bot

    @staticmethod
    def _check_indentical_channel(group, value):
        return value == config.get_value_channel(group)

    @staticmethod
    def _set_channel(group, channel):
        """
        Set name for main|public|sound channels

        Args:
            group: 'main', 'public', 'sound'
            channel: :class:`str` name of channel

        Returns: :class:`str`
            Message, what need to return in chat about status

        """

        if not Configuration._check_indentical_channel(group, channel):
            if group in config.list_of_channels:
                config.set_value_channel(group, channel)
                return ManagerMessages.get_message_succesfully_update_channel(group, channel)
            else:
                raise ValueError(f'Invalid argument value: use {config.list_of_channels}')
        else:
            return ManagerMessages.get_message_already_set_channel(group, channel)

    @commands.group(name='set')
    async def general_set(self, ctx: Context):
        """
        General command for set group

        Args:
            ctx: Context command of discord message

        """
        if ctx.invoked_subcommand is None:
            await ctx.send('Look on help for more info')

    @general_set.command(name='default')
    async def set_default(self, ctx: Context):
        config.set_default()
        await ctx.send(ManagerMessages.get_message_succesfully_set_default())

    @general_set.command(name='main')
    async def set_channel_main(self, ctx: Context, channel: str):
        if channel is not None:
            result = self._set_channel('main', channel)
            await ctx.send(result)

    @general_set.command(name='sound')
    async def set_channel_sound(self, ctx: Context, channel: str):
        if channel is not None:
            result = self._set_channel('sound', channel)
            await ctx.send(result)

    @general_set.command(name='public')
    async def set_channel_public(self, ctx: Context, channel: str):
        if channel is not None:
            result = self._set_channel('public', channel)
            await ctx.send(result)

    @staticmethod
    def _check_indentical_config_parametr(name, value: Bool):
        return bool(value) == config.get_config_boolean_value(name)

    @staticmethod
    def _set_config_boolean_value(name, value: Bool):
        if not Configuration._check_indentical_config_parametr(name, value):

            config.set_config_boolean_value(name, bool(value))

            return ManagerMessages.get_message_succesfully_update_config(name, value)
        else:
            return ManagerMessages.get_message_already_set_config(name, value)

    @staticmethod
    def _try_set_config_int_value(name, value):
        try:
            value = int(value)
            config.set_config_int_value(name, value)
        except ValueError:
            return ManagerMessages.get_message_not_int_or_on_off_value(value)
        else:
            return ManagerMessages.get_message_succesfully_update_config(name, value)

    @commands.command(name='autotake')
    async def autotake(self, ctx, value=None):
        """
        Command that work with autotake config
        Set | Get value for configuration bot

        Args:
            ctx: Context command of discord message
            value: Union[:class:`str` ['on', 'off'], :class:`int`]

        """
        if value is not None:
            if value in Bool.BOOLEAN_TRUE + Bool.BOOLEAN_FALSE:
                value = Bool(value)
                result = self._set_config_boolean_value('autotake', value)
                await ctx.send(result)
            else:
                result = self._try_set_config_int_value('autotake', value)
                await ctx.send(result)
        else:
            value = Bool(config.get_config_boolean_value('autotake'))
            await ctx.send(ManagerMessages.get_message_value_of_conf('autotake', value))

    @commands.command(name='conf')
    async def conf(self, ctx, value: bool = None):
        """
        Command that work with conf config
        Set | Get value for configuration bot

        Args:
            ctx: Context command of discord message
            value: :class:`str` ['on', 'off'] or other str -> bool values from DiscordAPI

        """
        if value is not None:
            result = self._set_config_boolean_value('conf', Bool(value))
            await ctx.send(result)
        else:
            value = Bool(config.get_config_boolean_value('conf'))
            await ctx.send(ManagerMessages.get_message_value_of_conf('conf', value))

    @commands.command(name='aa')
    async def aa(self, ctx, value=None):
        """
        Command that work with aa config
        Set | Get value for configuration bot

        Args:
            ctx: Context command of discord message
            value: Union[:class:`str` ['on', 'off'], :class:`int`]

        """
        if value is not None:
            if value in Bool.BOOLEAN_TRUE + Bool.BOOLEAN_FALSE:
                value = Bool(value)
                result = self._set_config_boolean_value('aa', value)
                await ctx.send(result)
            else:
                result = self._try_set_config_int_value('aa', value)
                await ctx.send(result)
        else:

            value = Bool(config.get_config_boolean_value('aa'))
            await ctx.send(ManagerMessages.get_message_value_of_conf('aa', value))
