import os
import telebot
from chatgpt.completions import completions
from chatgpt.edits import edits
from stable_diffusion.stable_diffusion import predict

main_menu_text = (
    "*Main Menu*\n"
    "Click */conversation* - _Start a new conversation_\n"
    "Click */images* - _Generate images by given prompt._\n"
    "Click */end* - _End the conversation or images._\n"
    "Click */help* - _You can use it for help_"
)

help_text = "*What you want to know?*"

conversation_help_text = (
    "/conversation\n"
    "   *start a conversation* - _You can use the conversation command or directly input something then start a conversation._\n"
    "   *new another conversation* - _If you want to end the current conversation and new a conversation, you can reuse the conversation command or end command_.\n"
)

images_help_text = (
    "/images\n"
    "   *generate images* - _You can use the images command then input something then generate images._\n"
    "   *generate images by edit* - _After you have generated a image, you can continue to input something and the bot will regenerate the image based on the previous image and your description._\n"
    "   *new another images* - _If you want to end the current images edtion and new a images, you can reuse the images command or end command_.\n"
)

button_description = {
    "conversation": "Let's start a converastion. You can ask me anything. If you want to new another the conversation, you need to click 'end' in the menu, otherwise, it will reply to you based on the previous content. ",
    "images": "Give me a prompt and I will generate an image.",
    "conversation_help": conversation_help_text,
    "images_help": images_help_text,
    "help": help_text,
}
previous_message_map = {}
previous_photo = None
mode = "conversation"


def bot_run():
    bot = telebot.TeleBot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    # bot.get_updates(1).clear()

    print("Authorized on account {}".format(os.getenv("TELEGRAM_BOT_TOKEN")))

    @bot.message_handler(commands=["start"])
    def start(message):
        # print(message)
        btn1 = telebot.types.InlineKeyboardButton(
            "Conversation", callback_data="conversation"
        )
        btn2 = telebot.types.InlineKeyboardButton("Images", callback_data="images")
        btn3 = telebot.types.InlineKeyboardButton("Help", callback_data="help")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.send_message(
            message.chat.id, main_menu_text, parse_mode="Markdown", reply_markup=markup
        )
        return

    @bot.message_handler(commands=["end"])
    @bot.message_handler(commands=["conversation"])
    def conversation_or_end(message):
        global previous_message_map, mode, previous_photo
        handle_previous_message(message.from_user.id)
        mode = "conversation"
        previous_photo = None
        if message.text == "/end":
            bot.send_message(
                message.chat.id,
                "Now you new another conversation or can generate another image",
            )
            return
        bot.send_message(message.chat.id, button_description["conversation"])
        return

    @bot.message_handler(commands=["images"])
    def images(message):
        global previous_photo, mode
        previous_photo = None
        mode = "images"
        bot.send_message(message.chat.id, button_description["images"])
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
        global previous_message_map, previous_photo, mode
        bot.answer_callback_query(call.id)
        if call.data == "conversation":
            handle_previous_message(call.from_user.id)
            mode = "conversation"
        elif call.data == "images":
            previous_photo = None
            mode = "images"
        elif call.data == "help":
            bot.edit_message_text(
                text=button_description[call.data],
                parse_mode="Markdown",
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=help_mark_up(),
            )
            return
        bot.send_message(
            call.message.chat.id,
            text=button_description[call.data],
            parse_mode="Markdown",
        )

    @bot.message_handler(content_types=["text"])
    @bot.edited_message_handler(content_types=["text"])
    def handle_text(message):
        global previous_message_map, previous_photo, mode
        bot.send_chat_action(message.chat.id, "typing")
        if mode == "conversation":
            if message.from_user.id not in previous_message_map:
                reply = completions(message.text)
                print("completions: ", reply)
            else:
                previous_message = previous_message_map[message.from_user.id]
                reply = edits(previous_message, message.text)
                # the reply contains the previous message so we need to remove it
                reply = reply.replace(previous_message, "")
                print("edits: ", reply)
            previous_message_map[message.from_user.id] = reply
            bot.send_message(message.chat.id, reply)
            return

        elif mode == "images":
            url = predict(message.text)
            reply = "The image url is \n" + url
            bot.send_message(message.chat.id, reply)
            return

    bot.infinity_polling()


def handle_previous_message(id):
    if id in previous_message_map:
        del previous_message_map[id]
    else:
        pass


def help_mark_up():
    btn1 = telebot.types.InlineKeyboardButton(
        "Conversation", callback_data="conversation_help"
    )
    btn2 = telebot.types.InlineKeyboardButton("Images", callback_data="images_help")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(btn1, btn2)
    return markup
