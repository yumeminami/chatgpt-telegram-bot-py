from utils.redis import get_redis_client
from telegram_bot.bot import get_bot
from user.user import update_user, get_user
import threading


def check_payment_update():
    redis_client = get_redis_client()
    email = redis_client.lpop("check_out_completed")
    if email != None:
        user_id = redis_client.hget("email_to_user_id", email)
        if user_id != None:
            user = get_user(user_id.decode())
            remain_token = user.remain_token
            update_user(user_id.decode(), remain_token=remain_token + 1000)
            bot = get_bot()
            bot.send_message(
                chat_id=user.chat_id,
                text="Your payment is completed. You have {} more tokens now.".format(
                    remain_token + 1000
                ),
                parse_mode="Markdown",
            )

    timer = threading.Timer(3, check_payment_update)
    timer.start()


# def check_out_complete_call_back(chat_id):
#     redis_client = get_redis_client()
