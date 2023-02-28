# from utils.redis import redis_client
from datetime import datetime
from utils.redis import get_redis_client
import json

user_map = {}


class User:
    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id
        self.mode = "conversation"
        self.conversation_history = ""
        self.expire_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.remain_token = 1000
        self.email = ""


def check_user(user_id, chat_id):
    redis_client = get_redis_client()
    user = redis_client.hget("user", user_id)

    if user is None:
        # new user
        user = User(user_id, chat_id)
        return True
    else:
        # existing user
        # check expire date and remain token
        if (user["remain_token"] <= 0) or (user["expire_date"] < datetime.now()):
            # no token or expired
            return False


def get_user(user_id):
    redis_client = get_redis_client()
    user_data = redis_client.hget("user", user_id)
    if user_data is None:
        return User(user_id, "")
    else:
        user_dict = json.loads(user_data)
        user_copy = User(user_dict["user_id"], user_dict["chat_id"])
        user_copy.mode = user_dict["mode"]
        user_copy.conversation_history = user_dict["conversation_history"]
        user_copy.expire_date = user_dict["expire_date"]
        user_copy.remain_token = user_dict["remain_token"]
        user_copy.email = user_dict["email"]
        return user_copy


def update_user(user_id, **kwargs):
    redis_client = get_redis_client()
    user_copy = get_user(user_id)
    if user_copy:
        for key, value in kwargs.items():
            setattr(user_copy, key, value)
        redis_client.hset("user", user_id, json.dumps(user_copy.__dict__, default=str))
    else:
        user_copy = User(user_id, None)
        for key, value in kwargs.items():
            setattr(user_copy, key, value)
        redis_client.hset("usery", user_id, json.dumps(user_copy.__dict__, default=str))
