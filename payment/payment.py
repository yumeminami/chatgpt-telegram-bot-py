from utils.redis import get_redis_client
from telegram_bot.bot import get_bot
from user.user import update_user, get_user
import threading
from datetime import datetime, timedelta
import json


def check_payment_update():
    redis_client = get_redis_client()
    email = redis_client.lpop("check_out_completed")
    if email != None:
        user_id = redis_client.hget("email_to_user_id", email)
        if user_id != None:
            user = get_user(user_id.decode())
            bot = get_bot()
            # check expire date is expired or not
            expire_date = datetime.strptime(
                user.expire_date, "%Y-%m-%d %H:%M:%S"
            )
            if expire_date < datetime.now():
                update_user(
                    user_id,
                    mode="chat",
                    expire_date=(datetime.now() + timedelta(days=30)).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                )
            else:
                update_user(
                    user_id,
                    mode="chat",
                    expire_date=(expire_date + timedelta(days=30)).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                )
            bot.send_message(
                chat_id=user.chat_id,
                text="Thank you for your payment. Your account has been extended for 30 days.",
                parse_mode="Markdown",
            )

    timer = threading.Timer(3, check_payment_update)
    timer.start()


def update_daily_limit():
    redis_client = get_redis_client()
    user_ids = redis_client.hgetall("user")
    for user_id, user_data in user_ids.items():
        user_id = user_id.decode()
        user_data = json.loads(user_data.decode())
        user_data["daily_limit"] = 20
        redis_client.hset("user", user_id, json.dumps(user_data))
