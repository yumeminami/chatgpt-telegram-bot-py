# from utils.redis import redis_client
from datetime import datetime
from utils.redis import get_redis_client
import json

user_map = {}


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.previous_message = ""
        self.mode = "ask"
        self.chat_history = []
        self.expire_date = datetime.now()
        self.remain_token = 1000
        self.email = ""


def check_user(user_id):
    redis_client = get_redis_client()
    user = redis_client.hget("user", user_id)

    if user is None:
        # new user
        user = {
            "user_id": user_id,
            "expire_date": datetime.now(),
            "remain_token": 1000,
            "chat_history": [],
            "email": "",
        }
        return True
    else:
        # existing user
        # check expire date and remain token
        if (user["remain_token"] <= 0) or (user["expire_date"] < datetime.now()):
            # no token or expired
            return False


def update_user(user_id, **kwargs):
    redis_client = get_redis_client()
    user = redis_client.hget("user", user_id)
    if user is None:
        # new user
        user = {
            "user_id": user_id,
            "email": "",
        }
    else:
        user = json.loads(user)
    for key, value in kwargs.items():
        user[key] = value
    redis_client.hset("user", user_id, json.dumps(user))
    return user


def get_user(user_id):
    redis_client = get_redis_client()
    user = redis_client.hget("user", user_id)
    if user is None:
        return None
    else:
        return json.loads(user)
