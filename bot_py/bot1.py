
import random
import telebot

from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


# Responses for different moods
MOOD_REPLIES = {
    "втомився": "😴 Не здавайся! Зроби невелику перерву!",
    "радію": "😄 Чудово! Продовжуй у тому ж дусі!",
    "боюся": "😨 Не хвилюйся, ти все зможеш!",
    "сумно": "😢 Не засмучуйся, завтра буде новий день!",
}

# Default responses
DEFAULT_REPLIES = [
    "Привіт, {name}!",
    "Ти все зможеш, {name}!",
    "Скоро початок завдання, {name}!",
]

# Secret word
SECRET_WORD = "артефакт"


# Create mood selection keyboard
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

keyboard.add(
    "😴 Втомився",
    "😄 Радію"
)

keyboard.add(
    "😨 Боюся",
    "😢 Сумно"
)


# Start command
@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name

    bot.send_message(
        message.chat.id,
        f"Привіт, {name}! Як ти сьогодні почуваєшся? Обери свій настрій:",
        reply_markup=keyboard
    )


# Handle messages
@bot.message_handler(func=lambda message: True)
def handle_any_message(message):
    text = message.text.lower() if message.text else ""
    name = message.from_user.first_name

    # Check secret word
    if SECRET_WORD in text:
        bot.send_message(
            message.chat.id,
            "🎉 Вітаю! Ти знайшов секретний артефакт!"
        )
        return

    # Check mood
    for mood, reply in MOOD_REPLIES.items():
        if mood in text:
            bot.send_message(
                message.chat.id,
                reply,
                reply_markup=keyboard
            )
            return

    # Default response
    reply = random.choice(DEFAULT_REPLIES)

    bot.send_message(
        message.chat.id,
        reply.format(name=name),
        reply_markup=keyboard
    )


# Run bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()
