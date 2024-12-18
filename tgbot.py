import telebot
from telebot import types

# Токен бота
BOT_TOKEN = "7560902568:AAEzvbfy76R0Vp0FSjmudNtNLkzvIL0eIl4"
bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище заметок
NOTES_FILE = "notes.txt"