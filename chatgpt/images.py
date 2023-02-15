import openai
import os


def images(prompt) -> str:
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Image.create(
            prompt=prompt,
            size="1024x1024",
        )
        return response["data"][0]["url"]
    except Exception as e:
        print(e)
        return "Error"
