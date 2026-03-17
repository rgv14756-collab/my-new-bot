import telebot
import os
from flask import Flask
from threading import Thread

# --- НАСТРОЙКИ RENDER (ОБЯЗАТЕЛЬНО) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()
# --------------------------------------

# ТВОИ ДАННЫЕ
BOT_TOKEN = "8792226891:AAEFBsz7W5EhI9xdr9oX6VgbasdSiBgYS4A"
ADMIN_CHAT_ID = "8668351155"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет👋\n"
        "Если хочешь добавить человека жми👉 /adduser\n"
        "Если хочешь выложить пост жми👉 /post\n"
        "Если хочешь удалить пост жми👉 /deletepost"
    )

@bot.message_handler(commands=['adduser'])
def adduser(message):
    bot.send_message(
        message.chat.id,
        "Мы рады новым подписчикам ☺️ вот ссылка на вступление.\n"
        "https://t.me/+QfaNhZzp4ZFjYTY6"
    )
    bot.register_next_step_handler(message, handle_adduser)

def handle_adduser(message):
    username = message.text.strip().lstrip('/').lstrip('@')
    try:
        bot.send_message(
            ADMIN_CHAT_ID,
            f"👤 Новый пользователь хочет добавить подписчика:\n@{username}\n\n"
            f"От: {message.from_user.first_name} (ID: {message.from_user.id})"
        )
    except Exception as e:
        print(f"Ошибка при отправке админу: {e}")
    bot.send_message(message.chat.id, "Отлично! Админ постарается добавить как можно скорее😉")

@bot.message_handler(commands=['post'])
def post(message):
    bot.send_message(
        message.chat.id,
        "Супер 👍 Выкладывай любые видео/фото связанные со школой. "
        "Администратор выложит твой пост в течение 24 часов🙃.\n"
        "‼️посты с учителями нельзя😢‼️"
    )
    bot.register_next_step_handler(message, handle_post)

SIGNATURE = "\n\nпредложка для ваших фото, видео, постов 👉 @podSlushan023_bot"

def handle_post(message):
    try:
        bot.send_message(ADMIN_CHAT_ID, f"📢 Новый пост от {message.from_user.first_name} (ID: {message.from_user.id}):")
        if message.content_type == 'text':
            bot.send_message(ADMIN_CHAT_ID, message.text + SIGNATURE)
        elif message.content_type in ('photo', 'video', 'animation', 'document'):
            original_caption = message.caption or ""
            bot.copy_message(ADMIN_CHAT_ID, message.chat.id, message.message_id, caption=original_caption + SIGNATURE)
        else:
            bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
            bot.send_message(ADMIN_CHAT_ID, SIGNATURE.strip())
    except Exception as e:
        print(f"Ошибка при отправке поста: {e}")
    bot.send_message(message.chat.id, "Отлично! Админ выставит твой пост как можно быстрее😁")

@bot.message_handler(commands=['deletepost'])
def deletepost(message):
    bot.send_message(message.chat.id, "Скинь пост который хочешь удалить🙃")
    bot.register_next_step_handler(message, handle_deletepost)

def handle_deletepost(message):
    try:
        bot.send_message(ADMIN_CHAT_ID, f"🗑 Запрос на удаление от {message.from_user.first_name}:")
        bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    except Exception as e:
        print(f"Ошибка удаления: {e}")
    bot.send_message(message.chat.id, "Выбранный пост удалят как можно быстрее!")

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Начать"),
    telebot.types.BotCommand("/adduser", "Добавить человека"),
    telebot.types.BotCommand("/post", "Выложить пост"),
    telebot.types.BotCommand("/deletepost", "Удалить пост"),
])

if __name__ == '__main__':
    keep_alive()  # Запуск веб-сервера для Render
    print("Бот запущен...")
    bot.infinity_polling(none_stop=True)
