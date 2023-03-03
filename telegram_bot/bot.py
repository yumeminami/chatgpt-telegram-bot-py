import telebot
from utils.redis import get_redis_client
from utils.token import count_token
from user.user import get_user, update_user
from telegram_bot.text import *
from chatgpt.chat import chat
from stable_diffusion.stable_diffusion import generate
import os

group_link = {"zh": "https://t.me/+F2l1Z3EeFVg5N2Y1"}


EMAIL_REGEX_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

bot = telebot.TeleBot(
    token=os.environ.get("TELEGRAM_BOT_TOKEN"),
    skip_pending=True,
    colorful_logs=True,
)


def get_bot():
    return bot


def main_menu_markup(language="en"):
    ask_button = telebot.types.InlineKeyboardButton(
        bot_text[language]["button_text"]["ask"], callback_data="ask"
    )
    chat_button = telebot.types.InlineKeyboardButton(
        bot_text[language]["button_text"]["chat"], callback_data="chat"
    )
    images_button = telebot.types.InlineKeyboardButton(
        bot_text[language]["button_text"]["images"], callback_data="images"
    )
    subscribe_button = telebot.types.InlineKeyboardButton(
        bot_text[language]["button_text"]["subscription"],
        callback_data="subscription",
    )
    language_button = telebot.types.InlineKeyboardButton(
        bot_text[language]["button_text"]["language"], callback_data="language"
    )
    help_button = telebot.types.InlineKeyboardButton(
        bot_text[language]["button_text"]["help"], callback_data="help"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(chat_button, ask_button, images_button)
    markup.add(subscribe_button)
    markup.add(language_button, help_button)
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    # print(message)
    user = get_user(message.from_user.id)
    markup = main_menu_markup(user.language)
    bot.send_message(
        message.chat.id,
        bot_text[user.language]["main_menu_text"],
        parse_mode="Markdown",
        reply_markup=markup,
    )
    return


@bot.message_handler(chat_types=["supergroup"])
def handle_supergroup(message):
    group_link_text = "[English](https://t.me/+7DN6wFZ90iA2NTZl)|[中文](https://t.me/+F2l1Z3EeFVg5N2Y1)|[繁体中文](https://t.me/+FYHiPmOLjeExNGNl)"
    bot.send_chat_action(message.chat.id, "typing")
    text = message.text
    if text.startswith("/ask") or text.startswith("ask"):
        response_message, success = chat([{"role": "user", "content": text}])
        if success == False:
            bot.send_message(message.chat.id, response_message)
            return
        bot.send_message(
            message.chat.id,
            response_message["content"] + "\n\n"
            "[English](https://t.me/+7DN6wFZ90iA2NTZl)|[中文](https://t.me/+F2l1Z3EeFVg5N2Y1)|[繁体中文](https://t.me/+FYHiPmOLjeExNGNl)",
            parse_mode="Markdown",
            reply_to_message_id=message.message_id,
        )
    else:
        bot.send_message(
            message.chat.id,
            "Please use /ask or ask the bot to ask something\n\n"
            "[English](https://t.me/+7DN6wFZ90iA2NTZl)|[中文](https://t.me/+F2l1Z3EeFVg5N2Y1)|[繁体中文](https://t.me/+FYHiPmOLjeExNGNl)",
            parse_mode="Markdown",
            reply_to_message_id=message.message_id,
        )
    return


@bot.message_handler(commands=["chat", "images", "ask"])
def command_handler(message):
    update_user(
        message.from_user.id,
        mode=message.text[1:],
        messages=[],
    )
    user = get_user(message.from_user.id)
    bot.send_message(
        message.chat.id,
        bot_text[user.language]["command_description_text"][message.text[1:]],
        parse_mode="Markdown",
    )
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


@bot.callback_query_handler(func=lambda call: call.data == "language")
def language(call):
    bot.answer_callback_query(call.id)
    en_language_button = telebot.types.InlineKeyboardButton(
        "🇺🇸English", callback_data="en"
    )
    zh_language_button = telebot.types.InlineKeyboardButton(
        "🇨🇳中文", callback_data="zh"
    )
    tranditional_chinese_button = telebot.types.InlineKeyboardButton(
        "🇭🇰繁體中文", callback_data="zh-hk"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(zh_language_button, tranditional_chinese_button)
    markup.add(en_language_button)
    # edit message
    user = get_user(call.from_user.id)
    bot.edit_message_text(
        text=bot_text[user.language]["choose_language_text"],
        parse_mode="Markdown",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )
    return


@bot.callback_query_handler(
    func=lambda call: call.data in ["en", "zh", "zh-hk"]
)
def set_language(call):
    bot.answer_callback_query(call.id)
    update_user(call.from_user.id, language=call.data)
    bot.edit_message_text(
        text=bot_text[call.data]["main_menu_text"],
        parse_mode="Markdown",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=main_menu_markup(call.data),
    )
    return


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    update_user(call.from_user.id, mode=call.data, messages=[])
    user = get_user(call.from_user.id)
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        text=bot_text[user.language]["command_description_text"][call.data],
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
                bot_text[user.language]["token_limit_text"],
                parse_mode="Markdown",
            )
            return
        response_message, success = chat([{"role": "user", "content": prompt}])
        if success == False:
            bot.send_message(message.chat.id, response_message)
            return
        bot.send_message(message.chat.id, response_message["content"])
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
        update_user(
            message.from_user.id,
            chat_id=message.chat.id,
            messages=user.messages,
        )
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
