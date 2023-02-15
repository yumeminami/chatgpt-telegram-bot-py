import os
import telebot
from chatgpt.completions import completions
from chatgpt.edits import edits
from chatgpt.images import images
from chatgpt.images_edit import images_edit

main_menu_text = "*Main Menu*\n" \
    "*/conversation* - _start a new conversation_\n" \
    "*/images* - _generate images by give prompt._\n" \
    "*/end* - _end the conversation or images_"

previous_message = None
previous_photo = None
mode = "conversation"


def bot_run():
    bot = telebot.TeleBot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

    @bot.message_handler(commands=['start'])
    def start(message):
        # print(message)
        btn1 = telebot.types.InlineKeyboardButton(
            'Conversation', callback_data='conversation')
        btn2 = telebot.types.InlineKeyboardButton(
            'Images', callback_data='images')
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, main_menu_text,
                         parse_mode='Markdown', reply_markup=markup)
        return

    @ bot.message_handler(commands=['end'])
    def end(message):
        global previous_message, previous_photo, mode
        previous_message = None
        previous_photo = None
        mode = 'conversation'
        bot.send_message(message.chat.id, "end")
        return

    @ bot.message_handler(commands=['conversation'])
    def conversation(message):
        global previous_message, mode
        previous_message = None
        mode = "conversation"
        bot.send_message(message.chat.id, "let's start a new conversation")
        return

    @ bot.message_handler(commands=['images'])
    def images(message):
        global previous_message, mode
        previous_message = None
        mode = "images"
        bot.send_message(
            message.chat.id, "give me a prompt and I will generate an image")
        return

    @ bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == 'conversation':
            bot.send_message(call.message.chat.id,
                             "let's start a new conversation")
        elif call.data == 'images':
            bot.send_message(call.message.chat.id,
                             "give me a prompt and I will generate an image")
        return

    @ bot.message_handler(content_types=['text'])
    def handle_text(message):
        global previous_message, mode
        bot.send_chat_action(message.chat.id, 'typing')
        if mode == "conversation":
            if previous_message is None:
                print('completions')
                reply = completions(message.text)
                bot.send_message(message.chat.id, reply)
                previous_message = reply
            else:
                print('edits')
                reply = edits(previous_message, message.text)
                # the reply contains the previous message so we need to remove it
                reply = reply.replace(previous_message, '')
                bot.send_message(message.chat.id, reply)
                previous_message = reply

        elif mode == "images":
            return

    @ bot.edited_message_handler(content_types=['text'])
    def handle_edited_text(message):
        bot.send_chat_action(message.chat.id, 'typing')
        global previous_message, mode
        if mode == "conversation":
            if previous_message is None:
                print('completions')
                reply = completions(message.text)
                bot.send_message(message.chat.id, reply)
                previous_message = reply
            else:
                print('edits')
                reply = edits(previous_message, message.text)
                bot.send_message(message.chat.id, reply)
                previous_message = reply

        elif mode == "images":
            return

    bot.infinity_polling()


def main_menu() -> str:

    return "Main Menu"
