from discord.ext.commands import CommandNotFound, MissingRequiredArgument, Cog, Context
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler


from call_bot.models import Base, engine
from call_bot.setting.botConfig import config_bot as config


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger_handler = RotatingFileHandler('discord.log', maxBytes=2**30, backupCount=1)  # 2**30 = 1Gb
logger_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)


class Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        Base.metadata.create_all(engine)
        logger.info('Bot connected to guild. Ready!')
        for channel in self.bot.get_all_channels():
            if channel.name == config.get_logging_channel_name():
                config.set_logging_channel(channel.name, channel.id)
                await channel.send(
                    '```'
                    f"{datetime.now().strftime('%H:%M:%S %d/%m/%Y')} "
                    f' {self.bot.user.name} '
                    'Ready'
                    '```'
                )

    @Cog.listener()
    async def on_command(self, ctx: Context):
        id_channel = config.get_logging_channel_id()
        logger.info(
            f' {ctx.bot.user.name} '
            f' \'{ctx.channel}\' '
            f' {ctx.author} '
            f' \'{ctx.message.content}\' '
        )
        await self.bot.get_channel(id_channel).send(
                '```'
                f"{datetime.now().strftime('%H:%M:%S %d/%m/%Y')} "
                f'{ctx.bot.user.name} '
                f'\'{ctx.channel}\' '
                f'{ctx.author} '
                f'\'{ctx.message.content}\''
                '```'
            )

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(error)
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f'U miss required parametr \'{error.param}\'')
        else:
            print(error)
            logger.error(f'{error}, {ctx.message}')
