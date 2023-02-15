import json
import os
from chatgpt.completions import completions
from chatgpt.edits import edits
from chatgpt.images import images
from telegram_bot.bot import bot_run
from config import init_config


def main():
    if not init_config():
        return
    bot_run()


if __name__ == '__main__':
    main()
