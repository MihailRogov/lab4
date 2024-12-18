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