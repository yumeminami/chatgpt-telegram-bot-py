from chatgpt.chat import chat


choice, flag = chat(
    [
        {"role": "user", "content": "Hello"},
        {"content": "Hello, how can I assist you today?", "role": "assistant"},
        {"role": "user", "content": "I want to buy a car"},
    ]
)

print(choice["content"])
