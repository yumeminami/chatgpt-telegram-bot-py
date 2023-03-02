import os
import openai


def chat(messages: list):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        print(response)
        return response.choices[0].message, True
    except Exception as e:
        print(e)
        return e, False
