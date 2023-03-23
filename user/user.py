# from utils.redis import redis_client
from datetime import datetime, timedelta
from utils.redis import get_redis_client
import json


class User:
    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id
        self.mode = "chat"
        self.expire_date = (datetime.now() + timedelta(days=7)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.email = ""
        self.language = "en"
        self.messages = []
        self.daily_limit = 20  # Set the default value for daily_limit


def check_user(user_id):
    redis_client = get_redis_client()
    user = redis_client.hget("user", user_id)

    if user is None:
        # new user
        user = User(user_id, "")
        return True
    else:
        user_dict = json.loads(user)
        if user_dict["mode"] == "expired":
            return False
        else:
            expire_date = datetime.strptime(
                user_dict["expire_date"], "%Y-%m-%d %H:%M:%S"
            )
            if expire_date < datetime.now():
                # update_user(user_id, mode="expired")
                return False
    return True


def get_user(user_id):
    redis_client = get_redis_client()
    user_data = redis_client.hget("user", user_id)
    if user_data is None:
        return User(user_id, "")
    else:
        user_dict = json.loads(user_data)
        user = User(user_dict["user_id"], user_dict["chat_id"])
        user.mode = user_dict["mode"]
        user.expire_date = user_dict["expire_date"]
        user.email = user_dict["email"]
        user.messages = user_dict["messages"]
        user.language = user_dict["language"]
        user.daily_limit = user_dict["daily_limit"]
        return user


def update_user(user_id, **kwargs):
    redis_client = get_redis_client()
    user = get_user(user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    redis_client.hset("user", user_id, json.dumps(user.__dict__, default=str))
