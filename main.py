from config import init_config
from telegram_bot.bot import get_bot
import time
import threading
from payment.payment import check_payment_update
import os

import logging
import fastapi
import uvicorn
import telebot


init_config()
bot = get_bot()
commands = bot.get_my_commands()
for command in commands:
    print(command.command + " - " + command.description)

WEBHOOK_PORT = int(
    os.environ.get("WEBHOOK_PORT")
)  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = "0.0.0.0"  # In some VPS you may need to put here the IP addr
start_time = int(time.time())

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

app = fastapi.FastAPI(docs=None, redoc_url=None)


@app.get("/")
def index():
    return "Hello World!"


url = "/{WEBHOOK_PORT}/webhook".format(WEBHOOK_PORT=WEBHOOK_PORT)
print(url)


@app.post(url)
def process_webhook(update: dict):
    """
    Process webhook calls
    """
    if update:
        print(update)
        # message = update.get("message")
        # # date = message.get("date")
        # if date < start_time:
        #     return
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(
    url="https://www.queenacheung.cn/{WEBHOOK_PORT}/webhook".format(
        WEBHOOK_PORT=WEBHOOK_PORT
    ),
    # certificate=open(WEBHOOK_SSL_CERT, "r"),
)

timer = threading.Timer(interval=5.0, function=check_payment_update)
timer.start()
# Process(target=check_payment_update).start()

uvicorn.run(
    app, host=WEBHOOK_LISTEN, port=WEBHOOK_PORT, timeout_keep_alive=300
)
