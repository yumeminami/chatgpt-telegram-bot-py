import openai
import os


def completions(prompt):
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        print(prompt)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
        )
        return response.choices[0].text
    except Exception as e:
        print(e)
        return "Error"
