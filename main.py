import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8792226891:AAHq5cTfbdGVf7QPlugEAnN1WhES3t_jDa8")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "8668351155")

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
        "Мы рады новым подписчикам ☺️Пришли никнейм своего друга/подруги.\n"
        "‼️убедитесь что человека можно добавлять в канал не по ссылке‼️"
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

    bot.send_message(
        message.chat.id,
        "Отлично! Админ постарается добавить как можно скорее😉"
    )


@bot.message_handler(commands=['post'])
def post(message):
    bot.send_message(
        message.chat.id,
        "Супер 👍Выкладывай любые видео/фото связаны со школой, разные забавные истории. "
        "Администратор выложит твой пост в течении 24 часов в телеграмм канал🙃.  "
        "‼️посты с учителями нельзя😢‼️"
    )
    bot.register_next_step_handler(message, handle_post)


SIGNATURE = "\n\nпредложка для ваших фото, видео, постов 👉@podSlushan023_bot"

def handle_post(message):
    try:
        bot.send_message(
            ADMIN_CHAT_ID,
            f"📢 Новый пост от {message.from_user.first_name} (ID: {message.from_user.id}):"
        )
        if message.content_type == 'text':
            bot.send_message(ADMIN_CHAT_ID, message.text + SIGNATURE)
        elif message.content_type in ('photo', 'video', 'animation', 'document'):
            original_caption = message.caption or ""
            new_caption = original_caption + SIGNATURE
            bot.copy_message(ADMIN_CHAT_ID, message.chat.id, message.message_id, caption=new_caption)
        else:
            bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
            bot.send_message(ADMIN_CHAT_ID, SIGNATURE.strip())
    except Exception as e:
        print(f"Ошибка при отправке поста админу: {e}")

    bot.send_message(
        message.chat.id,
        "Отлично! Админ выставит твой пост как можно быстрее😁"
    )


@bot.message_handler(commands=['deletepost'])
def deletepost(message):
    bot.send_message(
        message.chat.id,
        "Скинь пост который хочешь удалить🙃"
    )
    bot.register_next_step_handler(message, handle_deletepost)


def handle_deletepost(message):
    try:
        bot.send_message(
            ADMIN_CHAT_ID,
            f"🗑 Запрос на удаление поста от {message.from_user.first_name} (ID: {message.from_user.id}):"
        )
        bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    except Exception as e:
        print(f"Ошибка при отправке запроса на удаление: {e}")

    bot.send_message(
        message.chat.id,
        "Выбранный пост удалят как можно быстрее!"
    )


bot.set_my_commands([
    telebot.types.BotCommand("/start", "Начать"),
    telebot.types.BotCommand("/adduser", "Добавить человека"),
    telebot.types.BotCommand("/post", "Выложить пост"),
    telebot.types.BotCommand("/deletepost", "Удалить пост"),
])

print("Бот запущен...")
bot.polling(none_stop=True)
