"""tg_bot_en_v2.0
данный бот обращается к БД PostgreSQL и рандомно выдергивает из
таблички слова пользователю"""

import psycopg2
import telebot
import random
import surrogates

# ============================== Token ===================================

bot = telebot.TeleBot('6038347627:AAElmMizLc5UhgZBqWdqOz4V2ChD_Q9h***')

# ================================ BD ====================================

conn_db = psycopg2.connect(
    host="localhost",
    port="5439",
    database="sql_test",
    user="root",
    password="postgres",
)

# ================================ EMJ ====================================

rocket_emj = surrogates.decode('\ud83c\udfaf')
enflag_emj = surrogates.decode('\ud83c\uddfa\ud83c\uddf8')
fail_emj = surrogates.decode('\ud83e\udee5')
think_emj = surrogates.decode('\ud83e\udd14')
error_emj = surrogates.decode('	\ud83d\udea8')
chiken_enj = surrogates.decode('\ud83d\udc23')


# =========================================================================
# ======================== Заметки для логики =============================


# =========================================================================
# ========================== обращение к БД ===============================


def get_dict_en():
    dict_words = {}
    cur = conn_db.cursor()
    cur.execute("""SELECT word_en
                FROM english_words.eng_to_rus_words """)
    rows_ = cur.fetchall()
    key_en = 0
    for i in rows_:
        key_en += 1
        dict_words[key_en] = i[0]

    cur.execute("""SELECT word_ru
                FROM english_words.eng_to_rus_words """)
    rows_ = cur.fetchall()
    key_ru = 1000
    for i in rows_:
        key_ru += 1
        dict_words[key_ru] = i[0]
    return dict_words


# =========================================================================
# ============================ Telegram BOT ===============================

counter = 0
dict_from_bd = ''
num = 0


def send_en_word(message):
    global counter
    global dict_from_bd
    global num
    dict_from_bd = get_dict_en()
    counter = len(get_dict_en()) / 2
    num = random.randint(1, int(counter))
    bot.send_message(message.from_user.id, f'{enflag_emj}Переведите на EN  слово'
                                           f' - "{dict_from_bd[num]}"')


def answer_user(message):
    if message.text == dict_from_bd[num + 1000]:
        bot.reply_to(message, f'>>>> ВЕРНО! {rocket_emj}\n\n>>>> Следующее слово:')
        return send_en_word(message)
    else:
        bot.reply_to(message, f'>>>> ВЫ ОШИБЛИСЬ!')
        bot.send_message(message.from_user.id, f'{chiken_enj} Проверь себя, перевод '
                                               f'- "{dict_from_bd[num + 1000]}"')
        bot.send_message(message.from_user.id, '>>>> Попробуйте написать снова:')


def exception_key_value(message):
    bot.reply_to(message, 'Ошибка! Неверная команда!'
                          '\nНапишите "go" чтобы начать тренировку.')


# =========================================================================
# ========================== Логика Telegram BOT ==========================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот запущен!\n\nЯ буду отправлять "
                          "тебе слова/фразы на Английском,"
                          " а ты их переводи.\nЕсли ошибешься, "
                          "то я тебе напишу ответ \nОтправь - 'go' "
                          "для старта тренировки! ")


@bot.message_handler(commands=['hi'])
def send_welcome(message):
    bot.reply_to(message, "Рома, этот бот будет общедоступным для тренировке"
                          " Английский слов.\n Доступ пока дать не могу так "
                          "как он очень 'сырой' и требует доработки, но уже "
                          "пишет сам в телегу).")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        if message.text == "go":
            send_en_word(message)
        else:
            try:
                answer_user(message)
            except IndexError:
                exception_key_value(message)
    except KeyError:
        exception_key_value(message)


bot.polling()
