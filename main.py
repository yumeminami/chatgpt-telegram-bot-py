from config import init_config
from telegram_bot.bot import bot_run
from stable_diffusion.stable_diffusion import predict


def main():
    if not init_config():
        return
    # print(predict("expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli"))
    bot_run()


if __name__ == "__main__":
    main()
