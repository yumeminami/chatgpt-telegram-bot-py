from config import init_config
from telegram_bot.bot import run_bot

import threading
from payment.payment import check_payment_update


init_config()


if __name__ == "__main__":
    timer = threading.Timer(interval=5.0, function=check_payment_update)
    timer.start()
    run_bot()
