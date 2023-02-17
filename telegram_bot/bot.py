import os
import telebot
import logging
from chatgpt.completions import completions
from chatgpt.edits import edits
from stable_diffusion.stable_diffusion import generate
from user.user import User, user_map

main_menu_text = (
    "*Main Menu*\n"
    "Click */ask* - _Ask me anything._\n"
    "Click */conversation* - _Start a new conversation_\n"
    "Click */images* - _Generate images by given prompt._\n"
    "Click */end* - _End the conversation or images._\n"
    "Click */help* - _You can use it for help_\n"
    "\n"
    "Contact: zwqueena@163.com\n"
)

help_text = "*Click the button then will explain the relative function usage*"

ask_help_text = (
    "/ask\n"
    "   *ask me anything* - _You can use the ask command then input something then I will answer._\n"
)
conversation_help_text = (
    "/conversation\n"
    "   *start a conversation* - _You can use the conversation command and I will have a conversation with you. (PS: At present, the bot is still unable to memorize all your inputs, and can only generate reply based on its last reply and your latest input)_\n"
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
    "help": help_text,
}
user_map = {}


def bot_run():
    bot = telebot.TeleBot(
        token=os.getenv("TELEGRAM_BOT_TOKEN"),
        skip_pending=True,
        colorful_logs=True,
    )

    print("Authorized on account {}".format(os.getenv("TELEGRAM_BOT_TOKEN")))

    @bot.message_handler(commands=["start"])
    def start(message):
        # print(message)
        ask_button = telebot.types.InlineKeyboardButton("Ask", callback_data="ask")
        conversation_button = telebot.types.InlineKeyboardButton(
            "Conversation", callback_data="conversation"
        )
        images_button = telebot.types.InlineKeyboardButton(
            "Images", callback_data="images"
        )
        help_button = telebot.types.InlineKeyboardButton("Help", callback_data="help")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(ask_button, conversation_button, images_button)
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
            help_text,
            parse_mode="Markdown",
            reply_markup=help_mark_up(),
        )
        return

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        bot.answer_callback_query(call.id)
        if call.data == "help":
            bot.edit_message_text(
                text=button_description[call.data],
                parse_mode="Markdown",
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=help_mark_up(),
            )
            return
        update_user_map(call.from_user.id, mode=call.data)
        bot.send_message(
            call.message.chat.id,
            text=button_description[call.data],
            parse_mode="Markdown",
        )

    @bot.message_handler(content_types=["text"])
    @bot.edited_message_handler(content_types=["text"])
    def handle_text(message):
        bot.send_chat_action(message.chat.id, "typing")
        if message.from_user.id not in user_map:
            user_map[message.from_user.id] = User(message.from_user.id)

        user = user_map[message.from_user.id]

        if user.mode == "ask":
            print("ask")
            reply = completions(message.text)
            # sometimes the reply will start with the ? or . or !, so remove it
            if reply[0] in ["?", ".", "!"]:
                reply = reply[1:]
            bot.send_message(message.chat.id, reply)
            print("ask_reply: ", reply)
            return
        elif user.mode == "conversation":
            previous_message = user.previous_message
            if previous_message == "":
                reply = completions(message.text)
            else:
                reply = edits(previous_message, message.text)
                # remove the previous message in reply
                if previous_message in reply:
                    reply = reply.replace(previous_message, "")
            print("before conversation previous_message: ", previous_message)
            update_user_map(
                message.from_user.id, previous_message=reply, mode="conversation"
            )
            print(
                "after conversation previous_message: ",
                user_map[message.from_user.id].previous_message,
            )
            bot.send_message(message.chat.id, reply)
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

    bot.infinity_polling(logger_level=logging.DEBUG)


def help_mark_up():
    btn1 = telebot.types.InlineKeyboardButton(
        "Conversation", callback_data="conversation_help"
    )
    btn2 = telebot.types.InlineKeyboardButton("Images", callback_data="images_help")
    btn_3 = telebot.types.InlineKeyboardButton("Ask", callback_data="ask_help")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(btn_3, btn1, btn2)
    return markup


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
