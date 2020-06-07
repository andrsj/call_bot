from discord.ext.commands import Cog
from discord.ext import commands


from call_bot.setting.botConfig import Config
from call_bot.messages import ManagerMessages


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
    def _get_string_of_boolean(value: bool):
        return BOOLEAN_TRUE if value else BOOLEAN_FALSE

    @staticmethod
    def _check_indentical_channel(group, value):
        return value == Config.get_value_channel(group)

    @staticmethod
    def _set_channel(group, channel):
        if not Configuration._check_indentical_channel(group, channel):
            if group in Config.list_of_channels:
                Config.set_value_channel(group, channel)
                return ManagerMessages.get_message_succesfully_update_channel(group, channel)
            else:
                raise ValueError(f'Invalid argument value: use {Config.list_of_channels}')
        else:
            return ManagerMessages.get_message_already_set_channel(group, channel)

    @commands.command(name='set')
    async def setter(self, ctx, group, channel=None):
        if group in Config.list_of_channels:
            if channel is not None:
                result = self._set_channel(group, channel)
                await ctx.send(result)
            else:
                await ctx.send(ManagerMessages.get_message_miss_required_param_for_channels())
        elif group == 'default' and channel is None:
            Config.set_default()
            await ctx.send(ManagerMessages.get_message_succesfully_set_default())
        else:
            await ctx.send(ManagerMessages.get_message_not_found_set_group(group))

    @staticmethod
    def _check_indentical_config_parametr(name, value):
        return value == Config.get_config_boolean_value(name)

    def _set_config_boolean_value(self, name, value):
        if not Configuration._check_indentical_config_parametr(name, value):
            Config.set_config_boolean_value(name, value)
            value = self._get_string_of_boolean(value)
            return ManagerMessages.get_message_succesfully_update_config(name, value)
        else:
            value = self._get_string_of_boolean(value)
            return ManagerMessages.get_message_already_set_config(name, value)

    @staticmethod
    def _try_set_config_int_value(name, value):
        try:
            value = int(value)
            Config.set_config_int_value(name, value)
        except ValueError:
            return ManagerMessages.get_message_not_int_or_on_off_value(value)
        else:
            return ManagerMessages.get_message_succesfully_update_config(name, value)

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
            value = self._get_string_of_boolean(Config.get_config_boolean_value('autotake'))
            await ctx.send(ManagerMessages.get_message_value_of_conf('autotake', value))

    @commands.command(name='conf')
    async def conf(self, ctx, value: bool = None):
        if value is not None:
            result = self._set_config_boolean_value('conf', value)
            await ctx.send(result)
        else:
            value = self._get_string_of_boolean(Config.get_config_boolean_value('conf'))
            await ctx.send(ManagerMessages.get_message_value_of_conf('conf', value))

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
            value = self._get_string_of_boolean(Config.get_config_boolean_value('aa'))
            await ctx.send(ManagerMessages.get_message_value_of_conf('aa', value))
