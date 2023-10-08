"""tg_bot_en_v1.0
данный бот обращается к словарю питона и рандомно выдергивает из
него слова пользователю"""


import psycopg2
import telebot
import random
import surrogates


# ============================== Token ===================================

bot = telebot.TeleBot('6038347627:AAElmMizLc5UhgZBqWdqOz4V2ChD_Q9h***')

# ================================ EMJ ====================================

rocket_emj = surrogates.decode('\ud83c\udfaf')
enflag_emj = surrogates.decode('\ud83c\uddfa\ud83c\uddf8')
fail_emj = surrogates.decode('\ud83e\udee5')
think_emj = surrogates.decode('\ud83e\udd14')
error_emj = surrogates.decode('	\ud83d\udea8')
chiken_enj = surrogates.decode('\ud83d\udc23')

# =========================================================================
# ========================== Словарь слов =================================
# расширяй словарь для разных вариантов слов/фраз

dict_1 = {
    1: 'have a walk', 1001: 'прогуляться',
    2: 'have a look', 1002: 'посмотреть',
    3: 'have a bath', 1003: 'принять ванну',
    4: 'have a shower', 1004: 'принять душ',
    5: 'have a talk', 1005: 'поговорить',
    6: 'have a conversation', 1006: 'побеседовать',}

# =========================================================================
# ============================ Telegram BOT ===============================

num = 0


def send_en_word(message):
    global num
    num = random.randint(1001, 1006)
    bot.send_message(message.from_user.id, f'{enflag_emj}Переведите на EN  слово - "{dict_1[num]}"')


def answer_user(message):
    if message.text == dict_1[num - 1000]:
        bot.reply_to(message, f'>>>> ВЕРНО! {rocket_emj}\n\n>>>> Следующее слово:')
        return send_en_word(message)
    else:
        bot.reply_to(message, f'>>>> ВЫ ОШИБЛИСЬ!')
        bot.send_message(message.from_user.id, f'{chiken_enj} Проверь себя, перевод - "{dict_1[num - 1000]}"')
        bot.send_message(message.from_user.id, '>>>> Попробуйте написать снова:')


def exception_key_value(message):
    bot.reply_to(message, 'Ошибка! Неверная команда!'
                          '\nНапишите "go" чтобы начать тренировку.')


# =========================================================================
# ========================== Логика Telegram BOT ==========================


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот запущен!")


@bot.message_handler(commands=['hi'])
def send_welcome(message):
    bot.reply_to(message, "Рома, этот бот будет общедоступным для тренировке Английский слов.\n"
                          "Доступ пока дать не могу так как он очень 'сырой' и требует доработки,"
                          " но уже пишет сам в телегу).")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        if message.text == "go":
            send_en_word(message)
        else:
            answer_user(message)
    except KeyError:
        exception_key_value(message)


bot.polling()

