from utils.redis import get_redis_client
from telegram_bot.bot import get_bot
import threading


def check_payment_update():
    redis_client = get_redis_client()
    email = redis_client.lpop("check_out_completed")
    if email != None:
        print(email)
        chat_id = redis_client.hget("email_to_chat_id", email)
        bot = get_bot()
        bot.send_message(
            chat_id=chat_id.decode(),
            text="Thanks for your payment",
            parse_mode="Markdown",
        )

    timer = threading.Timer(3, check_payment_update)
    timer.start()
