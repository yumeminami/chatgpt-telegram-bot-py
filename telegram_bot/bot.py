import os
import telebot
from chatgpt.completions import completions
from chatgpt.edits import edits
from chatgpt.images import images as imgs
from chatgpt.images_edit import images_edit as imgs_edit

main_menu_text = (
    "*Main Menu*\n"
    "*/conversation* - _start a new conversation_\n"
    "*/images* - _generate images by give prompt._\n"
    "*/end* - _end the conversation or images_\n"
    "*/help* - _you can use it for help_"
)

help_text = "*What you want to know?*"

conversation_help_text = (
    "/conversation\n"
    "   *start a conversation* - _you can use the conversation command or directly input something then star a conversation._\n"
    "   *new another conversation* - _If you want to end the current conversation and new a conversation, you can reuse the conversation command or end command_.\n"
)

images_help_text = (
    "/images\n"
    "   *generate images* - _you can use the images command then input something then generate images._\n"
    "   *generate images by edit* - _After you have generated a image, you can continue to input something and the bot will regenerate the image based on the previous image and your description._\n"
    "   *new another images* - _If you want to end the current images edtion and new a images, you can reuse the images command or end command_.\n"
)
previous_message = None
previous_photo = None
mode = "conversation"


def bot_run():
    bot = telebot.TeleBot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

    @bot.message_handler(commands=["start"])
    def start(message):
        # print(message)
        btn1 = telebot.types.InlineKeyboardButton(
            "Conversation", callback_data="conversation"
        )
        btn2 = telebot.types.InlineKeyboardButton("Images", callback_data="images")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(btn1, btn2)
        bot.send_message(
            message.chat.id, main_menu_text, parse_mode="Markdown", reply_markup=markup
        )
        return

    @bot.message_handler(commands=["end"])
    def end(message):
        global previous_message, previous_photo, mode
        previous_message = None
        previous_photo = None
        mode = "conversation"
        bot.send_message(message.chat.id, "end")
        return

    @bot.message_handler(commands=["conversation"])
    def conversation(message):
        global previous_message, mode
        previous_message = None
        mode = "conversation"
        bot.send_message(message.chat.id, "conversation created.")
        return

    @bot.message_handler(commands=["images"])
    def images(message):
        global previous_message, mode
        previous_message = None
        mode = "images"
        bot.send_message(
            message.chat.id, "give me a prompt and I will generate an image"
        )
        return

    @bot.message_handler(commands=["help"])
    def help(message):
        btn1 = telebot.types.InlineKeyboardButton(
            "Conversation", callback_data="conversation_help"
        )
        btn2 = telebot.types.InlineKeyboardButton("Images", callback_data="images_help")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(btn1, btn2)
        bot.send_message(
            message.chat.id, help_text, parse_mode="Markdown", reply_markup=markup
        )
        return

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        global previous_message, previous_photo, mode
        if call.data == "conversation":
            bot.send_message(call.message.chat.id, "conversation created.")
            previous_message = None
            mode = "conversation"
        elif call.data == "images":
            bot.send_message(
                call.message.chat.id, "give me a prompt and I will generate an image"
            )
            previous_photo = None
            mode = "images"
        elif call.data == "conversation_help":
            bot.send_message(
                call.message.chat.id, text=conversation_help_text, parse_mode="Markdown"
            )
        elif call.data == "images_help":
            bot.send_message(
                call.message.chat.id, text=images_help_text, parse_mode="Markdown"
            )

        return

    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        global previous_message, previous_photo, mode
        bot.send_chat_action(message.chat.id, "typing")
        if mode == "conversation":
            if previous_message is None:
                print("completions")
                reply = completions(message.text)
                bot.send_message(message.chat.id, reply)
                previous_message = reply
            else:
                print("edits")
                reply = edits(previous_message, message.text)
                # the reply contains the previous message so we need to remove it
                reply = reply.replace(previous_message, "")
                bot.send_message(message.chat.id, reply)
                previous_message = reply
            return

        elif mode == "images":
            if previous_photo is None:
                print("images")
                url = imgs(message.text)
                reply = "The image url is \n" + url
                bot.send_message(message.chat.id, reply)
            else:
                print("images_edit")

            return

    @bot.edited_message_handler(content_types=["text"])
    def handle_edited_text(message):
        bot.send_chat_action(message.chat.id, "typing")
        global previous_message, mode
        if mode == "conversation":
            if previous_message is None:
                print("completions")
                reply = completions(message.text)
                bot.send_message(message.chat.id, reply)
                previous_message = reply
            else:
                print("edits")
                reply = edits(previous_message, message.text)
                bot.send_message(message.chat.id, reply)
                previous_message = reply

        elif mode == "images":
            return

    bot.infinity_polling()
