from config import init_config
from telegram_bot.bot import get_bot
import time
import threading
from payment.payment import check_payment_update, update_daily_limit
import os
import logging
import fastapi
import uvicorn
import telebot
import schedule

init_config()
bot = get_bot()
commands = bot.get_my_commands()
for command in commands:
    print(command.command + " - " + command.description)

WEBHOOK_PORT = int(os.environ.get("WEBHOOK_PORT"))
WEBHOOK_LISTEN = "0.0.0.0"
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
    if update:
        print(update)
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


bot.remove_webhook()

bot.set_webhook(
    url="https://www.queenacheung.cn/{WEBHOOK_PORT}/webhook".format(
        WEBHOOK_PORT=WEBHOOK_PORT
    ),
)


def daily_task():
    update_daily_limit()
    # add other daily tasks here


def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every().day.at("00:00").do(daily_task)

thread = threading.Thread(target=schedule_loop)
thread.start()

timer = threading.Timer(interval=5.0, function=check_payment_update)
timer.start()

uvicorn.run(
    app, host=WEBHOOK_LISTEN, port=WEBHOOK_PORT, timeout_keep_alive=300
)
