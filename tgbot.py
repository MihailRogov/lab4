import telebot
from telebot import types

# Токен бота
BOT_TOKEN = "7560902568:AAEzvbfy76R0Vp0FSjmudNtNLkzvIL0eIl4"
bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище заметок
NOTES_FILE = "notes.txt"
# Загрузка заметок из файла
def load_notes():
    notes = {}
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            user_id = None
            for line in file:
                line = line.strip()
                if line.startswith("User:"):
                    user_id = line.split(":")[1].strip()
                    notes[user_id] = []
                elif line and user_id:
                    notes[user_id].append(line)
    except FileNotFoundError:
        pass
    return notes

# Сохранение заметок в файл
def save_notes(notes_data):
    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        for user_id, user_notes in notes_data.items():
            file.write(f"User:{user_id}\n")
            for note in user_notes:
                file.write(f"{note}\n")
# Заметки пользователей
notes_data = load_notes()

# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Добавить заметку", "Посмотреть заметки", "Удалить заметку")
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для заметок. Выберите действие:",
        reply_markup=markup,
    )

# Добавление заметки
@bot.message_handler(func=lambda msg: msg.text == "Добавить заметку")
def add_note_start(message):
    msg = bot.send_message(message.chat.id, "Введите текст заметки:")
    bot.register_next_step_handler(msg, save_note)

def save_note(message):
    user_id = str(message.chat.id)
    note = message.text
    if user_id not in notes_data:
        notes_data[user_id] = []
    notes_data[user_id].append(note)
    save_notes(notes_data)
    bot.send_message(message.chat.id, f"Заметка добавлена: {note}")

# Просмотр заметок
@bot.message_handler(func=lambda msg: msg.text == "Посмотреть заметки")
def view_notes(message):
    user_id = str(message.chat.id)
    if user_id not in notes_data or not notes_data[user_id]:
        bot.send_message(message.chat.id, "У вас пока нет заметок.")
    else:
        notes = "\n".join(
            [f"{i + 1}. {note}" for i, note in enumerate(notes_data[user_id])]
        )
        bot.send_message(message.chat.id, f"Ваши заметки:\n{notes}")

# Удаление заметки
@bot.message_handler(func=lambda msg: msg.text == "Удалить заметку")
def delete_note_start(message):
    user_id = str(message.chat.id)
    if user_id not in notes_data or not notes_data[user_id]:
        bot.send_message(message.chat.id, "У вас пока нет заметок для удаления.")
        return
    notes = "\n".join(
        [f"{i + 1}. {note}" for i, note in enumerate(notes_data[user_id])]
    )
    msg = bot.send_message(
        message.chat.id, f"Ваши заметки:\n{notes}\nВведите номер заметки для удаления:"
    )
    bot.register_next_step_handler(msg, delete_note)

def delete_note(message):
    user_id = str(message.chat.id)
    try:
        note_id = int(message.text) - 1
        if 0 <= note_id < len(notes_data[user_id]):
            deleted_note = notes_data[user_id].pop(note_id)
            save_notes(notes_data)
            bot.send_message(
                message.chat.id, f"Заметка удалена: {deleted_note}"
            )
        else:
            bot.send_message(message.chat.id, "Заметка с таким номером не найдена.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер.")

# Запуск бота
bot.infinity_polling()