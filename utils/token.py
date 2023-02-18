import tiktoken


def count_token(prompt):
    enc = tiktoken.encoding_for_model("text-davinci-003")
    return len(enc.encode_ordinary(prompt))
