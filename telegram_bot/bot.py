import os
import telebot
import logging
from chatgpt.completions import completions
from stable_diffusion.stable_diffusion import generate
from user.user import User, get_user, update_user, user_map
from utils.token import count_token
from utils.redis import get_redis_client
from telegram_bot.text import (
    standard_subscripition,
    pro_subscription,
    subscription_note,
)


main_menu_text = (
    "*Main Menu*\n"
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
    "*Token limit*\n" "_Since the token of the current prompt has exceeded the limit_"
)

help_text = (
    "*Instruction:*\n" + ask_help_text + conversation_help_text + images_help_text
)

user_map = {}
MAX_TOKEN = 800
EMAIL_REGEX_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

bot = telebot.TeleBot(
    token="6212169703:AAExFIETNFl2lEQ9DeJkuJEsug0aLMSYBlE",
    skip_pending=True,
    colorful_logs=True,
)


def get_bot():
    return bot


def run_bot():
    print("Authorized on account {}".format(os.getenv("TELEGRAM_BOT_TOKEN")))
    # commands = bot.get_my_commands()
    # for command in commands:
    #     print(command.command + " - " + command.description)
    # update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    # bot.process_new_updates([update])

    @bot.message_handler(commands=["start"])
    def start(message):
        # print(message)
        ask_button = telebot.types.InlineKeyboardButton("💬Ask", callback_data="ask")
        conversation_button = telebot.types.InlineKeyboardButton(
            "📢Conversation", callback_data="conversation"
        )
        images_button = telebot.types.InlineKeyboardButton(
            "🎨Images", callback_data="images"
        )
        subscribe_button = telebot.types.InlineKeyboardButton(
            "🌟 Subscription", callback_data="subscription"
        )
        help_button = telebot.types.InlineKeyboardButton("❓Help", callback_data="help")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(ask_button, conversation_button, images_button)
        markup.add(subscribe_button)
        markup.add(help_button)
        bot.send_message(
            message.chat.id, main_menu_text, parse_mode="Markdown", reply_markup=markup
        )
        return

    @bot.message_handler(commands=["conversation", "images", "ask"])
    def command_handler(message):
        update_user_map(message.from_user.id, mode=message.text[1:])
        bot.send_message(message.chat.id, button_description[message.text[1:]])
        return

    @bot.message_handler(commands=["help"])
    def help(message):
        bot.send_message(
            message.chat.id,
            text=help_text,
            parse_mode="Markdown",
        )
        return

    # handle callback data is subscription
    @bot.callback_query_handler(func=lambda call: call.data == "subscription")
    def subscription(call):
        bot.answer_callback_query(call.id)
        user = get_user(call.from_user.id)
        print(user)
        if user is None:
            bot.send_message(
                text="Please enter your email address",
                parse_mode="Markdown",
                chat_id=call.message.chat.id,
            )

            return
        standard_subscription_button = telebot.types.InlineKeyboardButton(
            "💳Standard",
            url="https://buy.stripe.com/test_7sI3dufsW7KY1eo7st",
        )
        pro_subscription_button = telebot.types.InlineKeyboardButton(
            "💳PRO", url="https://buy.stripe.com/test_7sI3dufsW7KY1eo7st"
        )

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(standard_subscription_button, pro_subscription_button)
        bot.send_message(
            chat_id=call.message.chat.id,
            text=standard_subscripition
            + "\n"
            + pro_subscription
            + "\n"
            + subscription_note,
            parse_mode="Markdown",
            reply_markup=markup,
        )
        return

    @bot.callback_query_handler(func=lambda call: call.data == "help")
    def help(call):
        bot.answer_callback_query(call.id)
        bot.send_message(
            text=help_text,
            parse_mode="Markdown",
            chat_id=call.message.chat.id,
        )
        return

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        bot.answer_callback_query(call.id)
        update_user_map(call.from_user.id, mode=call.data)
        bot.send_message(
            call.message.chat.id,
            text=button_description[call.data],
            parse_mode="Markdown",
        )

    # handle email
    @bot.message_handler(regexp=EMAIL_REGEX_PATTERN)
    def handle_email(message):
        bot.send_chat_action(message.chat.id, "typing")
        user = get_user(message.from_user.id)
        redis_client = get_redis_client()
        if user is None:
            update_user(message.from_user.id, email=message.text)
            redis_client.hset(
                name="email_to_chat_id", key=message.text, value=message.chat.id
            )
            bot.send_message(
                text="Update email success.",
                parse_mode="Markdown",
                chat_id=message.chat.id,
            )

        else:
            update_user(message.from_user.id, email=message.text)
            redis_client.hset(
                name="email_to_chat_id", key=message.text, value=message.chat.id
            )
            bot.send_message(
                text="Update email success.",
                parse_mode="Markdown",
                chat_id=message.chat.id,
            )
        return

    @bot.message_handler(content_types=["text"])
    @bot.edited_message_handler(content_types=["text"])
    def handle_text(message):
        bot.send_chat_action(message.chat.id, "typing")
        if message.from_user.id not in user_map:
            user_map[message.from_user.id] = User(message.from_user.id)

        user = user_map[message.from_user.id]

        prompt = "Human: " + message.text + "\n" + "AI: "
        print("prompt token: ", count_token(prompt))
        if user.mode == "ask":
            print("ask")
            if count_token(prompt) > MAX_TOKEN:
                bot.send_message(
                    message.chat.id,
                    token_limit_text,
                    parse_mode="Markdown",
                )
                return
            reply = completions(prompt=prompt)
            bot.send_message(message.chat.id, reply)
            return
        elif user.mode == "conversation":
            print("conversation")
            previous_message = user.previous_message
            prompt = previous_message + prompt
            reply = completions(prompt=prompt)
            previous_message = prompt + reply + "\n"
            bot.send_message(message.chat.id, reply)
            print("previous_message token: ", count_token(previous_message))
            if count_token(previous_message) > MAX_TOKEN:
                bot.send_message(
                    message.chat.id,
                    token_limit_text,
                    parse_mode="Markdown",
                )
                bot.send_message(
                    message.chat.id,
                    "Here is your *conversation history*:\n" + previous_message,
                    parse_mode="Markdown",
                )
                update_user_map(message.from_user.id, mode="ask")
                return
            update_user_map(
                message.from_user.id,
                previous_message=previous_message,
                mode="conversation",
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

    bot.infinity_polling(skip_pending=True, logger_level=logging.DEBUG)


def update_user_map(id, **kwargs):
    global user_map
    try:
        del user_map[id]
    except:
        pass
    user_map[id] = User(id)
    for key, value in kwargs.items():
        setattr(user_map[id], key, value)
    return
