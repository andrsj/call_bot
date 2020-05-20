from call_bot import create_bot, settings


bot = create_bot()

if __name__ == '__main__':
    bot.run(settings.DISCORD_BOT_TOKEN)
