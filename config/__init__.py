import os
import json


def init_config():
    with open("config/config.json") as f:
        data = json.load(f)
    try:
        os.environ["OPENAI_API_KEY"] = data["openai_api_key"]
        os.environ["TELEGRAM_BOT_TOKEN"] = data["telegram_bot_token"]
        os.environ["REPLICATE_API_TOKEN"] = data["replicate_api_token"]
        os.environ["STABILITY_KEY"] = data["stability_key"]
        os.environ["STABILITY_HOST"] = "grpc.stability.ai:443"
        return True
    except Exception as e:
        print(e)
        return False
