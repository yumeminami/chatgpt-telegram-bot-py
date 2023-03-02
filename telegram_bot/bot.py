import telebot
from utils.redis import get_redis_client
from utils.token import count_token
from user.user import get_user, update_user
from telegram_bot.text import *
from chatgpt.completions import completions
from chatgpt.chat import chat
from stable_diffusion.stable_diffusion import generate
import os


main_menu_text = (
    "*OpenAI GPT-3.5 DALL-E Bot*(Beta)\n"
    "*NOTE*: _The bot now implements the GPT-3.5 model and real_ _*chat*_ _feature like ChatGPT._\n"
    "\n"
    "👋 Hi, I am a bot that uses OpenAI GPT-3 and DALL-E to help you.\n"
    "\n"
    "🤔 *What can I do?*\n"
    "🤖 Chat with me\n"
    "🔎 Find answers\n"
    "📚 Write academic essays\n"
    "💻 Programming code\n"
    "👩‍💻 Write emails and letters\n"
    "🌎 Translate and chat in any language\n"
    "🖼 Generate images\n"
    "\n"
    "*/chat* - _Have a conversation with me._\n"
    "\n"
    "*/ask* - _ Ask anything you want._\n"
    "\n"
    "*/images* - _Generate images with prompt._\n"
    "\n"
    "*/help* - _Find assistance for your querie._\n"
    "\n"
    "Contact: fengrongman@gmail.com\n"
)


ask_help_text = (
    "/ask\n"
    "   *ask me anything* - _You can use the ask command then input something then I will answer._\n"
)
chat_help_text = (
    "/chat\n"
    "   *start a chat* - _You can use the chat command and I will have a chat with you. "
)

images_help_text = (
    "/images\n"
    "   *generate images* - _You can use the images command then input something then generate images._\n"
)

button_description = {
    "ask": "You can ask me anything.",
    "chat": "Let's chat.",
    "images": "Give me a prompt and I will generate the image. The generation process may take a while.",
    "chat_help": chat_help_text,
    "images_help": images_help_text,
    "ask_help": ask_help_text,
    "help": "Instruction",
}

token_limit_text = (
    "*Token limit*\n"
    "_Since the token of the current prompt has exceeded the limit_\n"
    "_You can reduce the length of the input or start a new conversation with /chat_"
)

help_text = (
    "*Instruction:*\n" + ask_help_text + chat_help_text + images_help_text
)

user_map = {}
EMAIL_REGEX_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

bot = telebot.TeleBot(
    token=os.environ.get("TELEGRAM_BOT_TOKEN"),
    skip_pending=True,
    colorful_logs=True,
)


def get_bot():
    return bot


@bot.message_handler(commands=["start"])
def start(message):
    # print(message)
    ask_button = telebot.types.InlineKeyboardButton(
        "💬Ask", callback_data="ask"
    )
    chat_button = telebot.types.InlineKeyboardButton(
        "📢Chat", callback_data="chat"
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
    markup.add(chat_button, ask_button, images_button)
    markup.add(subscribe_button)
    markup.add(help_button)
    bot.send_message(
        message.chat.id,
        main_menu_text,
        parse_mode="Markdown",
        reply_markup=markup,
    )
    return


@bot.message_handler(commands=["chat", "images", "ask"])
def command_handler(message):
    update_user(
        message.from_user.id,
        mode=message.text[1:],
        messages=[],
    )
    bot.send_message(message.chat.id, button_description[message.text[1:]])
    return


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(
        message.chat.id,
        text="help",
        parse_mode="Markdown",
    )
    return


# # handle callback data is subscription
@bot.callback_query_handler(func=lambda call: call.data == "subscription")
def subscription(call):
    bot.answer_callback_query(call.id)
    # user = get_user(call.from_user.id)
    user = get_user(call.from_user.id)
    if user is None or user.email == "":
        bot.send_message(
            text="Please enter your email address",
            parse_mode="Markdown",
            chat_id=call.message.chat.id,
        )
        return
    standard_subscription_button = telebot.types.InlineKeyboardButton(
        "💳Standard",
        url="https://buy.stripe.com/test_fZecO494y0iw3mw3ce",
    )
    pro_subscription_button = telebot.types.InlineKeyboardButton(
        "💳PRO", url="https://buy.stripe.com/test_4gwcO44Oi1mA4qAaEH"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(standard_subscription_button, pro_subscription_button)
    bot.send_message(
        chat_id=call.message.chat.id,
        text=subscription_text,
        parse_mode="Markdown",
        reply_markup=markup,
    )
    return


@bot.callback_query_handler(func=lambda call: call.data == "help")
def help(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        text="help",
        parse_mode="Markdown",
        chat_id=call.message.chat.id,
    )
    return


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    update_user(call.from_user.id, mode=call.data, messages=[])
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        text=button_description[call.data],
        parse_mode="Markdown",
    )


# handle email
@bot.message_handler(regexp=EMAIL_REGEX_PATTERN)
def handle_email(message):
    bot.send_chat_action(message.chat.id, "typing")
    get_user(message.from_user.id)
    redis_client = get_redis_client()
    update_user(
        message.from_user.id, email=message.text, chat_id=message.chat.id
    )
    bot.send_message(
        text="Update email success.",
        parse_mode="Markdown",
        chat_id=message.chat.id,
    )
    redis_client.hset("email_to_user_id", message.text, message.from_user.id)
    redis_client.hset(
        name="email_to_chat_id", key=message.text, value=message.chat.id
    )
    return


@bot.message_handler(content_types=["text"])
@bot.edited_message_handler(content_types=["text"])
def handle_text(message):
    # tell user that bot is typing
    bot.send_chat_action(message.chat.id, "typing")
    # get user
    user = get_user(message.from_user.id)
    if user.mode == "ask":
        print("ask")
        prompt = message.text
        if count_token(prompt) > 1000:
            bot.send_message(
                message.chat.id,
                token_limit_text,
                parse_mode="Markdown",
            )
            return
        reply = completions(prompt=prompt)
        bot.send_message(message.chat.id, reply)
        return
    elif user.mode == "chat":
        print("chat")
        chat_message = {"role": "user", "content": message.text}
        user.messages.append(chat_message)
        response_message, success = chat(user.messages)
        if success == False:
            bot.send_message(message.chat.id, response_message)
            return
        user.messages.append(response_message)
        bot.send_message(message.chat.id, response_message["content"])
        update_user(message.from_user.id, messages=user.messages)
        return
    elif user.mode == "images":
        print("images")
        img_path = generate(message.text)
        bot.send_photo(
            message.chat.id,
            photo=telebot.types.InputFile(img_path),
            reply_to_message_id=message.message_id,
        )
        os.remove(img_path)
        return
