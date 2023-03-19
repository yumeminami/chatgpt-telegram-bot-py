# from chatgpt.chat import chat


# choice, flag = chat(
#     [
#         {"role": "user", "content": "Hello"},
#         {"content": "Hello, how can I assist you today?", "role": "assistant"},
#         {"role": "user", "content": "I want to buy a car"},
#     ]
# )

# print(choice["content"])
# from user.user import check_user

# print(check_user(2103115991))

# from chatgpt.moderation import moeradtions

# print(moeradtions("I want to buy a car"))
# print(moeradtions("I want to kill you"))
# from utils.redis import get_redis_client

# redis_client = get_redis_client()

# emails = redis_client.hgetall("email_to_user_id")

# for key,value in emails.items():
#     key = key.decode()
#     redis_client.sadd("emails", key)
