from user.user import User
import tiktoken

test_map = {}


def update(id, **kwargs):
    if id not in test_map:
        test_map[id] = User(id)
    for key, value in kwargs.items():
        setattr(test_map[id], key, value)


def main():
    # update(1)
    # # print test_map[1] all attributes
    # print(test_map[1].user_id)
    # print(test_map[1].previous_message)
    # print(test_map[1].mode)

    # update(1, previous_message="test")
    # print(test_map[1].user_id)
    # print(test_map[1].previous_message)
    # print(test_map[1].mode)

    # update(1, mode="images")
    # print(test_map[1].user_id)
    # print(test_map[1].previous_message)
    # print(test_map[1].mode)
    # print(count_words("我爱你"))
    enc = tiktoken.encoding_for_model("text-davinci-003")
    print(len(enc.encode_ordinary("")))


if __name__ == "__main__":
    main()
