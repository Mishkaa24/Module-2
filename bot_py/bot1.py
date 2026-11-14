import random

import telebot

from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

GUIDE_REPLIES = [
    "Привіт",
    "Скоро початок завдання, готуйся",
    "Ще не знаю що сказати",
    "Ти все зможеш",
]

@bot.message_handler(func=lambda message: True)
def handle_any_message(message):
    reply = random.choice(GUIDE_REPLIES)
    bot.send_message(message.chat.id, reply)

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()