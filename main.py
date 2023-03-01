from config import init_config
from telegram_bot.bot import get_bot

import threading
from payment.payment import check_payment_update


import logging
import fastapi
import uvicorn
import telebot

init_config()
bot = get_bot()
WEBHOOK_PORT = 8080  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = "0.0.0.0"  # In some VPS you may need to put here the IP addr


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

app = fastapi.FastAPI(docs=None, redoc_url=None)


@app.get("/")
def index():
    return "Hello World!"


@app.post("/terence_cheung/webhook")
def process_webhook(update: dict):
    """
    Process webhook calls
    """
    print(update)
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(
    url="https://www.queenacheung.cn/terence_cheung/webhook",
    # certificate=open(WEBHOOK_SSL_CERT, "r"),
)

timer = threading.Timer(interval=5.0, function=check_payment_update)
timer.start()

uvicorn.run(
    app, host=WEBHOOK_LISTEN, port=WEBHOOK_PORT, timeout_keep_alive=300
)
