import telebot
from utils.redis import get_redis_client
from user.user import get_user, update_user, check_user
from telegram_bot.text import *
from chatgpt.chat import chat
from chatgpt.moderation import moeradtions
from chatgpt.images import images
import os
import re
import threading

SUBSCRIPTION_PAYMENT_URL = (
    "https://buy.stripe.com/14k0420eu0wafWo144?prefilled_email="
)
# SUBSCRIPTION_PAYMENT_URL = (
#     "https://buy.stripe.com/test_5kAbIUg1seUy5cQfYY?prefilled_email="
# )
EMAIL_REGEX_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Initialize bot
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


def subscription_markup(email: str):
    standard_subscription_button = telebot.types.InlineKeyboardButton(
        "💳PAYMENT", url=SUBSCRIPTION_PAYMENT_URL + email
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(standard_subscription_button)
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    user = get_user(message.from_user.id)
    expire_date = user.expire_date
    user_subscription_info_text = bot_text[user.language][
        "user_subscription_info_text"
    ] + str("*" + expire_date + "*")
    markup = main_menu_markup(user.language)
    bot.send_message(
        message.chat.id,
        bot_text[user.language]["main_menu_text"]
        + "\n"
        + user_subscription_info_text
        + "\n\n"
        + "[Join our community](https://t.me/+jsIgjjZkobsyNjNl) and unlock the unlimited potential of our robots - ask away without any hesitation!",
        parse_mode="Markdown",
        reply_markup=markup,
        disable_web_page_preview=True,
    )
    return


@bot.message_handler(
    commands=["chat", "images", "ask"], chat_types=["private"]
)
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
            reply_markup=telebot.types.ForceReply(selective=True),
        )
        return
    bot.send_message(
        chat_id=call.message.chat.id,
        text=subscription_text,
        parse_mode="Markdown",
        reply_markup=subscription_markup(email=user.email),
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
def handle_email(message):
    email = message.text
    if re.match(EMAIL_REGEX_PATTERN, email) is None:
        return "Please enter a valid email address"
    get_user(message.from_user.id)
    redis_client = get_redis_client()
    email = email[: email.index("@")].lower() + email[email.index("@") :]
    if redis_client.sadd("emails", email) == 0:
        return "This email address has been used"
    update_user(message.from_user.id, email=email, chat_id=message.chat.id)
    redis_client.hset("email_to_user_id", email, message.from_user.id)
    return "Thank you for your email address"


@bot.message_handler(chat_types=["supergroup"])
def handle_supergroup(message):
    bot.send_chat_action(message.chat.id, "typing")
    text = message.text
    if text.startswith("/ask") or text.startswith("ask"):
        if moeradtions(message.text) is True:
            bot.send_message(
                message.chat.id,
                bot_text[user.language]["forbidden_word_text"],
                parse_mode="Markdown",
            )
            return
        response_message, success = chat([{"role": "user", "content": text}])
        if success == False:
            bot.send_message(message.chat.id, response_message)
            return
        bot.send_message(
            message.chat.id,
            response_message["content"] + "\n\n",
            parse_mode="Markdown",
            reply_to_message_id=message.message_id,
        )
    else:
        bot.send_message(
            message.chat.id,
            "Please use /ask or ask the bot to ask something\n\n",
            parse_mode="Markdown",
            reply_to_message_id=message.message_id,
        )
    return


@bot.message_handler(content_types=["text"], chat_types=["private"])
@bot.edited_message_handler(content_types=["text"], chat_types=["private"])
def handle_text(message):
    # Create a new thread to handle the message
    threading.Thread(target=handle_text_thread, args=(message,)).start()


def handle_text_thread(message):
    # tell user that bot is typing
    bot.send_chat_action(message.chat.id, "typing")
    # handle email
    if (
        message.reply_to_message is not None
        and message.reply_to_message.text == "Please enter your email address"
    ):
        response = handle_email(message)
        bot.send_message(
            chat_id=message.chat.id,
            text=response,
            parse_mode="Markdown",
        )
        if response == "Thank you for your email address":
            bot.send_message(
                chat_id=message.chat.id,
                text=subscription_text,
                parse_mode="Markdown",
                reply_markup=subscription_markup(email=message.text),
            )
        return
    # get user
    user = get_user(message.from_user.id)
    if user.daily_limit == 0 and check_user(message.from_user.id) == False:
        bot.send_message(
            message.chat.id,
            "Sorry, you have reached the daily limit. Please try again tomorrow. or you could just use 10HKD to subscribe to unlock unlimited experience.",
            reply_markup=subscription_markup(email=user.email),
            parse_mode="Markdown",
        )
        return

    if moeradtions(message.text) is True:
        bot.send_message(
            message.chat.id,
            bot_text[user.language]["forbidden_word_text"],
            parse_mode="Markdown",
        )
        return
    daily_limit_tips = "Dayily limit: *" + str(user.daily_limit-1) + "/20*"
    if user.mode == "ask":
        print("ask")
        prompt = message.text
        response_message, success = chat([{"role": "user", "content": prompt}])
        if success == False:
            bot.send_message(message.chat.id, response_message)
            return
        bot.send_message(message.chat.id, response_message["content"]+"\n\n"+daily_limit_tips, parse_mode="Markdown")
        update_user(message.from_user.id, daily_limit=user.daily_limit - 1)
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
        bot.send_message(message.chat.id, response_message["content"]+"\n\n"+daily_limit_tips, parse_mode="Markdown")
        update_user(
            message.from_user.id,
            chat_id=message.chat.id,
            messages=user.messages,
            daily_limit=user.daily_limit - 1,
        )
        return
    elif user.mode == "images":
        print("images")
        url = images(message.text)
        if url is None:
            bot.send_message(
                message.chat.id,
                "Sorry, I can't find any images for your query",
                parse_mode="Markdown",
            )
            return

        bot.send_message(
            message.chat.id,
            url,
            parse_mode="Markdown",
        )
        # img_path = generate(message.text)
        # bot.send_photo(
        #     message.chat.id,
        #     photo=telebot.types.InputFile(img_path),
        #     reply_to_message_id=message.message_id,
        # )
        # os.remove(img_path)
        return
