import yaml

configfile = open('bot.yaml')
config = yaml.full_load(configfile)

DISCORD_CLIENT_ID = config['DISCORD_CLIENT_ID']
DISCORD_BOT_TOKEN = config['DISCORD_BOT_TOKEN']


__all__ = ['DISCORD_BOT_TOKEN', 'DISCORD_CLIENT_ID', ]
