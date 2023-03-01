import telebot

ASK_MODE = "ask"
CONVERSATION_MODE = "conversation"
IMAGE_MODE = "images"
TRANSLATE_MODE = "translate"
ASK_EMAIL_MODE = "ask_email"

main_menu_text = (
    "*OpenAI GPT-3 DALL-E Bot*(Beta)\n"
    "*NOTE*: _The bot is still in beta, and the service is not stable. If you encounter any problems, please contact me._\n"
    "\n"
    "👋 Hi, I am a bot that uses OpenAI GPT-3 and DALL-E to help you.\n"
    "🤔 *What can I do?*\n"
    "🔎 Find answers\n"
    "📚 Write academic essays\n"
    "💻 Programming code\n"
    "👩‍💻 Write emails and letters\n"
    "🌎 Translate and chat in any language\n"
    "🖼 Generate images\n"
    "\n"
    "Click */ask* - _Ask me anything._\n"
    "\n"
    "Click */conversation* - _Start a new conversation_\n"
    "\n"
    "Click */images* - _Generate images by given prompt._\n"
    "\n"
    "Click */help* - _You can use it for help_\n"
    "\n"
    "Contact: fengrongman@gmail.com\n"
)


ask_help_text = (
    "/ask\n"
    "   *ask me anything* - _You can use the ask command then input something then I will answer._\n"
)
conversation_help_text = (
    "/conversation\n"
    "   *start a conversation* - _You can use the conversation command and I will have a conversation with you. "
    "(PS: Currently, the maximum token count permitted for a conversation is 1000, which roughly translates to 700 words. "
    "When the limit is exceeded, the bot will prompt you and output a log of your conversation.)_\n"
)

images_help_text = (
    "/images\n"
    "   *generate images* - _You can use the images command then input something then generate images._\n"
)

button_description = {
    "ask": "You can ask me anything.",
    "conversation": "Let's start a converastion.",
    "images": "Give me a prompt and I will generate the image. The generation process may take a while.",
    "conversation_help": conversation_help_text,
    "images_help": images_help_text,
    "ask_help": ask_help_text,
    "help": "Instruction",
}

token_limit_text = (
    "*Token limit*\n"
    "_Since the token of the current prompt has exceeded the limit_"
)

help_text = (
    "*Instruction:*\n"
    + ask_help_text
    + conversation_help_text
    + images_help_text
)

user_map = {}
MAX_TOKEN = 800
EMAIL_REGEX_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

bot = telebot.TeleBot(
    token="6212169703:AAExFIETNFl2lEQ9DeJkuJEsug0aLMSYBlE",
    skip_pending=True,
    colorful_logs=True,
)

# print("Authorized on account {}".format(os.getenv("TELEGRAM_BOT_TOKEN")))
# commands = bot.get_my_commands()
# for command in commands:
#     print(command.command + " - " + command.description)


def get_bot():
    return bot


@bot.message_handler(commands=["start"])
def start(message):
    # print(message)
    ask_button = telebot.types.InlineKeyboardButton(
        "💬Ask", callback_data="ask"
    )
    conversation_button = telebot.types.InlineKeyboardButton(
        "📢Conversation", callback_data="conversation"
    )
    images_button = telebot.types.InlineKeyboardButton(
        "🎨Images", callback_data="images"
    )
    subscribe_button = telebot.types.InlineKeyboardButton(
        "🌟 Subscription(TEST)", callback_data="subscription"
    )
    help_button = telebot.types.InlineKeyboardButton(
        "❓Help", callback_data="help"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(ask_button, conversation_button, images_button)
    markup.add(subscribe_button)
    markup.add(help_button)
    bot.send_message(
        message.chat.id,
        main_menu_text,
        parse_mode="Markdown",
        reply_markup=markup,
    )
    return


# @bot.message_handler(commands=["conversation", "images", "ask"])
# def command_handler(message):
#     update_user(
#         message.from_user.id,
#         mode=message.text[1:],
#         conversation_history="",
#     )
#     bot.send_message(message.chat.id, button_description[message.text[1:]])
#     return
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(
        message.chat.id,
        text=help_text,
        parse_mode="Markdown",
    )
    return


# # handle callback data is subscription
# @bot.callback_query_handler(func=lambda call: call.data == "subscription")
# def subscription(call):
#     bot.answer_callback_query(call.id)
#     # user = get_user(call.from_user.id)
#     user = get_user(call.from_user.id)
#     if user is None or user.email == "":
#         bot.send_message(
#             text="Please enter your email address",
#             parse_mode="Markdown",
#             chat_id=call.message.chat.id,
#         )
#         return
#     standard_subscription_button = telebot.types.InlineKeyboardButton(
#         "💳Standard",
#         url="https://buy.stripe.com/test_fZecO494y0iw3mw3ce",
#     )
#     pro_subscription_button = telebot.types.InlineKeyboardButton(
#         "💳PRO", url="https://buy.stripe.com/test_4gwcO44Oi1mA4qAaEH"
#     )
#     markup = telebot.types.InlineKeyboardMarkup()
#     markup.add(standard_subscription_button, pro_subscription_button)
#     bot.send_message(
#         chat_id=call.message.chat.id,
#         text=subscription_text,
#         parse_mode="Markdown",
#         reply_markup=markup,
#     )
#     return
@bot.callback_query_handler(func=lambda call: call.data == "help")
def help(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        text=help_text,
        parse_mode="Markdown",
        chat_id=call.message.chat.id,
    )
    return


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     update_user(call.from_user.id, mode=call.data, conversation_history="")
#     bot.answer_callback_query(call.id)
#     bot.send_message(
#         call.message.chat.id,
#         text=button_description[call.data],
#         parse_mode="Markdown",
#     )
# # handle email
# @bot.message_handler(regexp=EMAIL_REGEX_PATTERN)
# def handle_email(message):
#     bot.send_chat_action(message.chat.id, "typing")
#     get_user(message.from_user.id)
#     redis_client = get_redis_client()
#     update_user(
#         message.from_user.id, email=message.text, chat_id=message.chat.id
#     )
#     bot.send_message(
#         text="Update email success.",
#         parse_mode="Markdown",
#         chat_id=message.chat.id,
#     )
#     redis_client.hset(
#         "email_to_user_id", message.text, message.from_user.id
#     )
#     redis_client.hset(
#         name="email_to_chat_id", key=message.text, value=message.chat.id
#     )
#     return
# @bot.message_handler(content_types=["text"])
# @bot.edited_message_handler(content_types=["text"])
# def handle_text(message):
#     # tell user that bot is typing
#     bot.send_chat_action(message.chat.id, "typing")
#     # get user
#     user = get_user(message.from_user.id)
#     prompt = "Human: " + message.text + "\nAI: "
#     print("prompt token: ", count_token(prompt))
#     if user.mode == "ask":
#         print("ask")
#         if count_token(prompt) > MAX_TOKEN:
#             bot.send_message(
#                 message.chat.id,
#                 token_limit_text,
#                 parse_mode="Markdown",
#             )
#             return
#         reply = completions(prompt=prompt)
#         bot.send_message(message.chat.id, reply)
#         return
#     elif user.mode == "conversation":
#         print("conversation")
#         conversation_history = user.conversation_history
#         prompt = conversation_history + prompt
#         reply = completions(prompt=prompt)
#         conversation_history = prompt + reply + "\n"
#         bot.send_message(message.chat.id, reply)
#         print(
#             "conversation_history token: ",
#             count_token(conversation_history),
#         )
#         if count_token(conversation_history) > MAX_TOKEN:
#             bot.send_message(
#                 message.chat.id,
#                 token_limit_text,
#                 parse_mode="Markdown",
#             )
#             bot.send_message(
#                 message.chat.id,
#                 "Here is your *conversation history*:\n"
#                 + conversation_history,
#                 parse_mode="Markdown",
#             )
#             update_user(message.from_user.id, conversation_history="")
#             return
#         update_user(
#             message.from_user.id, conversation_history=conversation_history
#         )
#         return
#     elif user.mode == "images":
#         print("images")
#         img_path = generate(message.text)
#         bot.send_photo(
#             message.chat.id,
#             photo=telebot.types.InputFile(img_path),
#             reply_to_message_id=message.message_id,
#         )
#         os.remove(img_path)
#         return
