
import random
import telebot

from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


# -------------------------
# DATA
# -------------------------

MOOD_REPLIES = {
    "втомився": "😴 Не здавайся! Зроби невелику перерву!",
    "радію": "😄 Чудово! Продовжуй у тому ж дусі!",
    "боюся": "😨 Не хвилюйся, ти все зможеш!",
    "сумно": "😢 Не засмучуйся, завтра буде новий день!",
}

DEFAULT_REPLIES = [
    "Привіт, {name}!",
    "Ти все зможеш, {name}!",
    "Скоро початок завдання, {name}!",
]

SECRET_WORD = "артефакт"

QUEST_TASKS = [
    "Знайди стару мапу, що веде до загубленого водоспаду.",
    "Допоможи мандрівнику відшукати його загублений компас.",
    "Перетни чарівний ліс і принеси звідти незвичайний листок.",
    "Розгадай загадку біля руїн старого замку.",
    "Знайди таємну стежку на вершину гори до заходу сонця.",
]

INVENTORY_POOL = [
    "чарівний компас",
    "старовинна мапа",
    "кришталевий амулет",
    "зілля сміливості",
    "золотий ключ",
    "чарівний ліхтар",
]

# New: Riddles for the traveler
RIDDLES = [
    "🧩 Я завжди показую шлях, але сам нікуди не йду. Що я? (Компас)",
    "🧩 Мене розгортають, щоб знайти дорогу, але я не маю ніг. Що я? (Мапа)",
    "🧩 Я високо в небі, освітлюю шлях мандрівникам уночі. Що я? (Місяць)",
]


# -------------------------
# KEYBOARD
# -------------------------

keyboard = telebot.types.ReplyKeyboardMarkup(
    resize_keyboard=True
)

keyboard.add("😴 Втомився", "😄 Радію")
keyboard.add("😨 Боюся", "😢 Сумно")


# -------------------------
# HELP TEXT
# -------------------------

HELP_TEXT = (
    "📜 Що вміє твій провідник:\n\n"
    "/start - познайомитися з провідником\n"
    "/help - показати цю довідку\n"
    "/quest - отримати завдання на подорож\n"
    "/inventory або /bag - переглянути наплічник\n"
    "/riddle - отримати загадку мандрівника\n"
    "/dice - кинути кубик долі\n"
    "/gift [ім'я] - подарувати магічний сувенір\n\n"
    "Або просто напиши мені будь-яке повідомлення!"
)


# -------------------------
# COMMANDS
# -------------------------

@bot.message_handler(commands=["start"])
def handle_start(message):
    name = message.from_user.first_name

    text = (
        f"Вітаю у світі пригод, {name}! 🗺️\n"
        "Я твій особистий провідник у цьому квесті.\n"
        "Напиши /help, щоб подивитися мої можливості."
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=keyboard
    )


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(
        message.chat.id,
        HELP_TEXT,
        reply_markup=keyboard
    )


@bot.message_handler(commands=["quest"])
def handle_quest(message):
    task = random.choice(QUEST_TASKS)

    bot.send_message(
        message.chat.id,
        f"🗺️ Твоє завдання:\n\n{task}"
    )


# Inventory with two command names
@bot.message_handler(commands=["inventory", "bag"])
def handle_inventory(message):
    items = random.sample(INVENTORY_POOL, 3)

    inventory_text = "🎒 Твій наплічник:\n" + "\n".join(
        f"• {item}" for item in items
    )

    bot.send_message(message.chat.id, inventory_text)


# New: Riddle command
@bot.message_handler(commands=["riddle"])
def handle_riddle(message):
    riddle = random.choice(RIDDLES)

    bot.send_message(
        message.chat.id,
        riddle
    )


# New: Dice command
@bot.message_handler(commands=["dice"])
def handle_dice(message):
    number = random.randint(1, 6)

    bot.send_message(
        message.chat.id,
        f"🎲 Кубик долі показав: {number}! Твоя удача зростає."
    )


# New: Gift command with an argument
@bot.message_handler(commands=["gift"])
def handle_gift(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) > 1 and parts[1].strip():
        name = parts[1].strip()

        bot.send_message(
            message.chat.id,
            f"🎁 Провідник передає магічний сувенір для {name}!"
        )
    else:
        bot.send_message(
            message.chat.id,
            "⚠️ Вкажи ім'я після команди!\n"
            "Правильний формат: /gift [ім'я]"
        )


# -------------------------
# GENERAL MESSAGES
# -------------------------

@bot.message_handler(func=lambda message: True)
def handle_any_message(message):

    if not message.text:
        return

    text = message.text.lower()
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


# -------------------------
# RUN BOT
# -------------------------

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
