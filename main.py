from config import init_config
from telegram_bot.bot import bot_run


def main():
    if not init_config():
        return
    # print(predict("expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli"))
    bot_run()
    # print(completions("hello"))


if __name__ == "__main__":
    main()
