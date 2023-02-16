from config import init_config
from telegram_bot.bot import bot_run


def main():
    if not init_config():
        return
    bot_run()


if __name__ == "__main__":
    main()
