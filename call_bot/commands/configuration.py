from discord.ext.commands import Cog
from discord.ext import commands
import yaml

from call_bot.setting.botConfig import Config


BOOLEAN_TRUE = 'on'
BOOLEAN_FALSE = 'off'


class Configuration(Cog):
    def __int__(self, bot):
        self.bot = bot

    @staticmethod
    def _get_boolean(value):
        if value == BOOLEAN_TRUE:
            return True
        elif value == BOOLEAN_FALSE:
            return False
        else:
            raise ValueError(f'Invalid argument value: use [\'{BOOLEAN_TRUE}\' or \'{BOOLEAN_FALSE}\']')

    @staticmethod
    def _check_indentical_channel(group, value):
        return value == Config.get_value_channel(group)

    @staticmethod
    def _set_channel(group, channel):
        if not Configuration._check_indentical_channel(group, channel):
            if group in Config.list_of_channels:
                Config.set_value_channel(group, channel)
                return f'\'{group}\' succesfully update to \'{channel}\''
            else:
                raise ValueError(f'Invalid argument value: use {Config.list_of_channels}')
        else:
            return f'\'{group}\' is already set \'{channel}\''

    @commands.command(name='set')
    async def setter(self, ctx, group, channel=None):
        if group in Config.list_of_channels and channel is not None:
            result = self._set_channel(group, channel)
            await ctx.send(result)
        elif group == 'default' and channel is None:
            Config.set_default()
            await ctx.send('Bot configuration succesfully set to default values')
        else:
            await ctx.send('Not found group')

    @staticmethod
    def _check_indentical_config_parametr(name, value):
        return value == Config.get_config_boolean_value(name)

    @staticmethod
    def _set_config_boolean_value(name, value):
        if not Configuration._check_indentical_config_parametr(name, value):
            Config.set_config_boolean_value(name, value)
            value = 'on' if value else 'off'
            return f'Config \'{name}\' succsesfully updated to \'{value}\''
        else:
            return f'Config \'{name}\' already set to \'{value}\''

    @staticmethod
    def _try_set_config_int_value(name, value):
        try:
            value = int(value)
            Config.set_config_int_value(name, value)
        except ValueError:
            return f'\'{value}\' -> it is not int or \'on\\off\' value'
        else:
            return f'\'{name}\' succesfully updated to \'{value}\''

    @commands.command(name='autotake')
    async def autotake(self, ctx, value=None):
        if value is not None:
            if value in [BOOLEAN_TRUE, BOOLEAN_FALSE]:
                value = self._get_boolean(value)
                result = self._set_config_boolean_value('autotake', value)
                await ctx.send(result)
            else:
                result = self._try_set_config_int_value('autotake', value)
                await ctx.send(result)
        else:
            value = 'on' if Config.get_config_boolean_value('autotake') else 'off'
            await ctx.send(f'Autotake: {value}')

    @commands.command(name='conf')
    async def conf(self, ctx, value: bool = None):
        if value is not None:
            result = self._set_config_boolean_value('conf', value)
            await ctx.send(result)
        else:
            value = 'on' if Config.get_config_boolean_value('conf') else 'off'
            await ctx.send(f'Conf: {value}')

    @commands.command(name='aa')
    async def aa(self, ctx, value=None):
        if value is not None:
            if value in [BOOLEAN_TRUE, BOOLEAN_FALSE]:
                value = self._get_boolean(value)
                result = self._set_config_boolean_value('aa', value)
                await ctx.send(result)
            else:
                result = self._try_set_config_int_value('aa', value)
                await ctx.send(result)
        else:
            value = 'on' if Config.get_config_boolean_value('aa') else 'off'
            await ctx.send(f'Aa: {value}')
