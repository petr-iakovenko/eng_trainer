import psycopg2
import random

conn_db = psycopg2.connect(
        host="localhost",
        port="5439",
        database="sql_test",
        user="root",
        password="postgres",
)

cursor = conn_db.cursor()
cursor.execute("""SELECT id, word_en, flag_forgot 
               FROM english_words.eng_to_rus_words 
               WHERE flag_forgot = 1 
               ORDER BY id 
               LIMIT 100;""")
rows = cursor.fetchall()
print('=============================================================='
      '\nСтатистика:\nСлово/Фраза - Удачных попыток - Вызов помощи')
for row in rows:
    print(f'"{row[0]}" - {row[1]} - {row[2]}')

def add_word_db_en(word):
    """to update word on eng"""
    list_ = []
    cur = conn_db.cursor()
    cur.execute("""SELECT word_en 
                FROM english_words.eng_to_rus_words 
                WHERE word_en = %s""", (word,))
    row = cur.fetchall()
    if row == list_:
        cur.execute("""INSERT INTO english_words.eng_to_rus_words (word_en) 
                    VALUES (%s)""", (word,))
        conn_db.commit()
    else:
        pass


def add_translate_word_db_en(word, translate):
    """to update translate word on rus"""
    cur = conn_db.cursor()
    cur.execute("""UPDATE english_words.eng_to_rus_words 
                SET word_ru = %s 
                WHERE word_en = %s """, (translate, word,))
    conn_db.commit()


def add_word_db_ru(word):
    """добавляет в БД слова RU"""
    list_ = []
    cur = conn_db.cursor()
    cur.execute("""SELECT word 
                FROM russian_words.words 
                WHERE word = %s""", (word,))
    row = cur.fetchall()
    if row == list_:
        cur.execute("""insert into russian_words.words (word) 
                    VALUES (%s)""", (word,))
        conn_db.commit()
    else:
        pass


def statistic_word_right(word):
    """to update counter correct response"""
    cur = conn_db.cursor()
    cur.execute("""UPDATE english_words.eng_to_rus_words  
                SET countet_try = countet_try + 1
                WHERE word_en = %s""", (word,))
    conn_db.commit()
    cur.execute("""SELECT countet_try 
                FROM english_words.eng_to_rus_words 
                WHERE word_en = %s""", (word,))
    rows = cur.fetchall()
    # print(*rows)
    if rows[0][0] == 10:
        cur.execute("""UPDATE english_words.eng_to_rus_words 
                    SET flag_forgot = 0 
                    WHERE word_en = %s""", (word,))
        conn_db.commit()


def statistic_word_help(word):
    """to update counter run 'помощь'"""
    cur = conn_db.cursor()
    cur.execute("""UPDATE english_words.eng_to_rus_words  
                SET countet_try = 0 
                WHERE word_en = %s""", (word,))
    conn_db.commit()
    cur.execute("""UPDATE english_words.eng_to_rus_words  
                SET counter_forgot = counter_forgot + 1 
                WHERE word_en = %s""", (word,))
    conn_db.commit()
    

def flag_forgot(word): 
    cur = conn_db.cursor()
    cur.execute("""UPDATE english_words.eng_to_rus_words  
                SET flag_forgot = 1 
                WHERE word_en = %s""", (word,))
    conn_db.commit()


def add_points(points_, flag):
    """to update counter points"""
    if flag == True:
        points_ += 1
        print('>>>> ВЕРНО! +1 point.')
    else:
        print('>>>> ВЫ ОШИБЛИСЬ! -5 points')
        points_ -= 5
        print('\n==================================================\n>>>> СЧЕТ:'
              f'{points_} points.'
              '\nПопробуй еще раз! \n(чтобы показать ответ набери "помощь")!'
              '\n==================================================')
    if points_ % 10 == 0:
        print(f'>>>> Твой результат ---------> {points_} очков.')
    elif points_ == 21:
        print(f'Поздравляю!\nТвой результат {points_} очков'
              '\nПоменяй сложность если слишком легко.')
    return points_   


dict_pol_les_preply = {
    1: 'unemployed', 1001: 'безработный',
    2: 'decide', 1002: 'решать',
    3: 'set up', 1003: 'создать',
    4: 'look for', 1004: 'искать',
    5: 'sacked/fired sack(мешок)', 1005: 'уволенный',
    6: 'applied for', 1006: 'подал заявку на',
    7: 'overtime', 1007: 'сверхурочные',
    8: 'got promoted', 1008: 'повысили',
    9: 'work shifts', 1009: 'рабочая смена',
    10: 'was made redundant', 1010: 'уволили',
    11: 'resign', 1011: 'уйти с работы',
    12: 'retire', 1012: 'уйти на пенсию',
    13: 'go with', 1013: 'встречаться с',
    14: 'go ahead', 1014: 'продолжать',
    15: 'have a glass of wine', 1015: 'выпить стакан вина',
    16: 'have a headache', 1016: 'страдать от головной боли',
    17: 'take up', 1017: 'заняться',
    18: 'Are you satisfied?', 1018: 'доволен?',
    19: 'Do you hear?', 1019: 'слышишь?',
    20: 'take a look', 1020: 'взгляни',
    21: 'arrive', 1021: 'прибывать',
    22: 'depart', 1022: 'покидать',
    23: 'Which one?', 1023: 'какую?',
    24: 'Have you heard?', 1024: 'ты слышал?',
    25: 'to suppose', 1025: 'предполагать',
    26: 'to suggest', 1026: 'предлагать',
    27: 'to escape', 1027: 'убегать',
    28: 'to be able', 1028: 'быть в состоянии',
    29: 'to abuse', 1029: 'оскорблять',
    30: 'to consist of', 1030: 'состоять из',
    31: 'to guess', 1031: 'думать',
    32: 'to accept', 1032: 'согласовать',
    33: 'to advise', 1033: 'советовать',
    34: 'to allow', 1034: 'разрешать',
    35: 'to conclude', 1035: 'включать в себя',
    36: 'to settle', 1036: 'поселиться',
    37: 'Monday', 1037: 'понедельник',
    38: 'Tuesday', 1038: 'вторник',
    39: 'Wednesday', 1039: 'среда',
    40: 'Thursday', 1040: 'четверг',
    41: 'Friday', 1041: 'пятница',
    42: 'Saturday', 1042: 'суббота',
    43: 'Sunday', 1043: 'воскресенье',
    44: 'to assure', 1044: 'убеждать',
    45: 'to avoid', 1045: 'избегать',
    46: 'to receive', 1046: 'получать',
    47: 'to remain', 1047: 'напоминать',
    48: 'to retain', 1048: 'удержать',
    49: 'to obtain', 1049: 'получить; добиться',
    50: 'to waste', 1050: 'тратить впустую',
    51: 'to prefer', 1051: 'предпочитать',
    52: 'to explain', 1052: 'объяснять',
    53: 'latency', 1053: 'задержка',
    54: 'subquery', 1054: 'подзапрос',
    55: 'additional', 1055: 'дополнительный',
    56: 'enroll', 1056: 'поступить',
    57: 'attempt', 1057: 'попытка',
    58: 'Precision', 1058: 'точность',
    59: 'confident', 1059: 'уверенный',
    60: 'environment', 1060: 'окружающая среда; обстановка',
    61: 'impress', 1061: 'впечатлить',
    62: "Let's continue", 1062: 'продолжим',
    63: 'prove', 1063: 'докажи',
    64: 'essential', 1064: 'важный',
    65: 'carry out', 1065: 'выполнять',
    66: 'Can you handle it?', 1066: 'справишься?',
    67: 'pressure', 1067: 'давление',
    68: 'take action', 1068: 'принять решение',
    69: 'provide', 1069: 'предусматривать',
    70: 'I believe', 1070: 'верю',
    71: 'mention', 1071: 'упоминание',
    72: 'match', 1072: 'соответствовать',
    73: 'solve', 1073: 'решить(проблему)',
    74: 'contribute', 1074: 'делать вклад',
    75: 'rest', 1075: 'отдых',
    76: 'hold it', 1076: 'подержи',
    77: 'not for long', 1077: 'ненадолго',
    78: 'foreign', 1078: 'зарубежный; внешний',
    79: 'abroad', 1079: 'за границей',
    80: 'collaborate', 1080: 'сотрудничать',
    81: 'upstairs', 1081: 'наверху',
    82: 'jointly', 1082: 'совместно',
    83: 'produce', 1083: 'производить',
    84: 'design', 1084: 'намерение',
    85: 'succeed', 1085: 'добиться успеха',
    86: 'hire', 1086: 'нанимать',
    87: 'determine', 1087: 'определять',
    88: 'cool down', 1088: 'остынь',
    89: 'wage', 1089: 'заработная плата',
    90: 'refer to', 1090: 'ссылаться на',
    91: 'brief', 1091: 'краткий',
    92: 'quality', 1092: 'качество',
    93: 'state', 1093: 'состояние',
    94: 'lack', 1094: 'недостаток; отсутствие',
    95: 'continuous', 1095: 'непрерывный',
    96: 'ahead', 1096: 'впереди',
    97: 'seek', 1097: 'искать',
    98: 'advice', 1098: 'совет; рекомендация',
    99: 'stand out', 1099: 'выделяться',
    100: 'Do you feel it?', 1100: 'чувствуешь?',
    101: 'honest', 1101: 'честный; подленный',
    102: 'relate', 1102: 'устанавливать связь между',
    103: 'direct', 1103: 'направлять',
    104: 'slight', 1104: 'легкий',
    105: 'similar', 1105: 'похожий',
    106: 'whole', 1106: 'целое',
    107: 'enjoy', 1107: 'наслаждайся',
    108: 'give up on trying', 1108: 'отказаться от попыток',
    109: 'passionate about', 1109: 'увлечен',
    110: 'include', 1110: 'содержит',
    111: 'jealousy', 1111: 'ревность; зависть',
    112: 'overall', 1112: 'общий; в целом',
    113: 'loud', 1113: 'громкий',
    114: 'Can you imagine?', 1114: 'представляешь?',
    115: 'handle setbacks', 1115: 'справляться с неудачами',
    116: 'I confirm', 1116: 'подтверждаю',
    117: "Let's get started", 1117: 'приступим',
    118: 'sign in', 1118: 'войдите',
    119: 'capable', 1119: 'способный',
    120: 'let me go', 1120: 'пусти',
    121: 'huge disaster', 1121: 'огромная катастрофа',
    122: 'able', 1122: 'способный',
    123: 'self-awareness', 1123: 'самосознание',
    124: 'improve', 1124: 'улучшать',
    125: 'outcome', 1125: 'результат',
    126: 'prevent', 1126: 'предотвратить',
    127: 'actions', 1127: 'действие',
    128: 'have a seat', 1128: 'присаживайся',
    129: 'blame', 1129: 'винить',
    130: 'respond', 1130: 'отвечать реагировать',
    131: 'admitting', 1131: 'признание',
    132: 'shortcoming', 1132: 'недостаток',
    133: 'humble', 1133: 'скромный',
    134: 'validating', 1134: 'проверка',
    135: 'willing', 1135: 'готовый',
    136: 'that', 1136: 'что',
    137: 'overcome', 1137: 'преодолеть',
    138: 'regarding', 1138: 'относительно',
    139: 'above', 1139: 'вышесказанный',
    140: 'impressed', 1140: 'впечатлен',
    141: 'could be', 1141: 'может быть',
    142: 'fit for', 1142: 'подходит для',
    143: 'represents', 1143: 'представляет(описание)',
    144: 'leading', 1144: 'ведущий; передовой',
    145: 'revenue', 1145: 'доход',
    146: 'available', 1146: 'доступный',
    147: 'improving', 1147: 'улучшение',
    148: 'calidating', 1148: 'проверка',
    149: 'expanding', 1149: 'расширение',
    150: 'apart', 1150: 'отдельно',
    151: 'confirming', 1151: 'подтверждающий',
    152: 'provider', 1152: 'поставщик',
    153: 'collecting', 1153: 'сбор',
    154: 'set', 1154: 'набор',
    155: 'explain', 1155: 'объяснять',
    156: 'what did you mean?', 1156: 'что ты имел ввиду?',
    157: 'he is bored', 1157: 'он утомленный',
    158: 'Where it does hurt?', 1158: 'где болит?',
    159: 'It got cold', 1159: 'похолодало',
    160: 'hurt', 1160: 'больно',
    161: "I'm looking at", 1161: 'я смотрю на',
    162: "I'm looking after", 1162: 'я присматриваю за',
    163: "I'm looking for", 1163: 'я ищу',
    164: "I'm waiting for my friend", 1164: 'жду своего друга',
    165: 'fast faster fastest', 1165: 'быстрый быстрее самый быстрый',
    166: 'better', 1166: 'лучший',
    167: 'well', 1167: 'хорошо',
    168: 'it takes time', 1168: 'это занимает время',
    169: 'crucial', 1169: 'ключевой',
    170: 'tips', 1170: 'советы',
    171: 'way', 1171: 'способ',
    172: 'impress', 1172: 'впечатлить',
    173: 'assess', 1173: 'оценить',
    174: 'trap', 1174: 'ловушка',
    175: 'fall', 1175: 'падать',
    176: 'immediately', 1176: 'немедленно',
    177: 'adopt', 1177: 'принять',
    178: 'attitude', 1178: 'позиция в ситуации',
    179: 'decision', 1179: 'решение',
    180: 'enjoy', 1180: 'наслаждаться',
    181: 'surroundings', 1181: 'окружение',
    182: 'condition', 1182: 'состояние условие',
    183: 'environment', 1183: 'окружающая среда обстановка',
    184: 'impress', 1184: 'впечатлить',
    185: 'good at', 1185: 'хорош в',
    186: 'advance', 1186: 'продвигаться',
    187: 'to set goal', 1187: 'устанавливать цель',
    188: 'few / several', 1188: 'несколько',
    189: 'on a call', 1189: 'на переговорах',
    190: 'point out', 1190: 'указать',
    191: 'since then', 1191: 'с того времени',
    192: 'neglect', 1192: 'пренебрегать',
    193: 'resolve', 1193: 'решить',
    194: 'growth', 1194: 'рост',
    195: 'regret', 1195: 'сожаление',
    196: 'grab', 1196: 'использовать',
    197: 'several', 1197: 'несколько',
    198: 'tight dedaline', 1198: 'жесткие сроки',
    199: 'instead', 1199: 'вместо',
    200: 'commit', 1200: 'совершать',
    201: 'agreement', 1201: 'соглашение',
    202: 'effort', 1202: 'попытка',
    203: 'nerves', 1203: 'нервы',
}


def dif_choice():
    """run choice difficulty"""
    print('\n\n============= программа "Тренажер английского v2.0" запущена =============\n\n')
    while True:
        print('Выбери сложность:\nTranslate B1 words to RUS:'
              '\n\t1 - B1 words to RUS'
              '\n\t2 - B1 forgotten_words to RUS'
              '\n\t3 - SELECT forgotten dict'
              '\n\n\t Clear - clear f_dict / Update - update f_dict')
        difficulty = (input('Выбрана сложность: ').strip())
        if difficulty == '1':
            print('\n"1 - B1 words to RUS"'
                  '\n-- переводите фразы на англиский язык; '
                  '\n- за правильный ответ ты получишь +1 '
                  'point и -5 points если ошибешься.')
            return diff_1()
        elif difficulty == '2':
            print('\n"2 - B1 forgotten_words to RUS"'
                  '\n-- переводите фразы на англиский язык; '
                  '\n- за правильный ответ ты получишь +1 '
                  'point и -5 points если ошибешься.')
            return diff_2()
        elif difficulty == 'Clear':
            print('Обчистка таблицы forgotten_word запущена!!!')
            return clear_forgotten_table()
        elif difficulty == 'Update':
            print('Добавление новых забытых слов')
            return insert_new_forgotten_words()
        elif difficulty == '3':
            return get_forgotten_dict()
        else:
            print('ОШИБКА ВВОДА!\n\n\n')
    

def forgotten_words():
    """return dict(key=num, value=word) from database"""
    dict_forgotten_word = {}
    cur = conn_db.cursor()
    cur.execute("""SELECT word_en 
                FROM english_words.forgot_en_words """)
    rows = cur.fetchall()
    key_en = 0
    for i in rows:
        key_en += 1
        dict_forgotten_word[key_en] = i[0]

    cur.execute("""SELECT word_ru 
                FROM english_words.forgot_en_words """)
    rows = cur.fetchall()
    key_ru = 1000
    for i in rows:
        key_ru += 1
        dict_forgotten_word[key_ru] = i[0]
    return dict_forgotten_word


def diff_1():
    points_ = 0
    while True:
        num = random.randint(1, 203)
        while True:
            print(f'\nEn: {dict_pol_les_preply[num]}')
            word = dict_pol_les_preply[num]
            add_word_db_en(word)
            res = input('Ru: ').strip()
            if res == dict_pol_les_preply[num + 1000]:
                statistic_word_right(word)
                add_translate_word_db_en(word, res)
                points_ = add_points(points_, True)
                break
            elif res == 'Выход' or res == 'выход':
                conn_db.close()
                print(f'\n\nТренировка завершена!'
                      f'\n>>>> Твой результат ---------> {points_} очков. ')
                return '============= программа выключена ============='
            elif res == 'Помощь' or res == 'помощь':
                print(f'----- подсказка: {dict_pol_les_preply[num + 1000]}')
                statistic_word_help(word)
                flag_forgot(word)
            else:
                points_ = add_points(points_, False)


def statistic_forgotten_word_right(word):
    """to update counter correct response"""
    cur = conn_db.cursor()
    cur.execute("""UPDATE english_words.forgot_en_words  
                SET countet_try = countet_try + 1
                WHERE word_en = %s""", (word,))
    conn_db.commit()
    cur.execute("""SELECT countet_try 
                FROM english_words.forgot_en_words 
                WHERE word_en = %s""", (word,))
    rows = cur.fetchall()
    # print(*rows)
    if rows[0][0] == 10:
        cur.execute("""UPDATE english_words.forgot_en_words 
                    SET flag_forgot = 0 
                    WHERE word_en = %s""", (word,))
        conn_db.commit()

def know_word_en(word_en):
    """ return TRUE if word is learning """
    cur = conn_db.cursor()
    cur.execute("""SELECT countet_try 
                FROM english_words.forgot_en_words 
                WHERE word_en = %s;""", (word_en,))
    rows = cur.fetchall()
    if rows[0][0] == 2: # счетчик для статуса запоминания
        return True
    return False

def diff_2():
    points_ = 0
    counter = len(forgotten_words()) / 2
    while True:
        dict_forgotten = forgotten_words()
        num = random.randint(1, counter) 
        if know_word_en(dict_forgotten[num]) == True: # если слово выучено
            pass
        else:
            while True:
                print(f'\nEn: {dict_forgotten[num]}')
                word = dict_forgotten[num]
                res = input('Ru: ').strip()
                if res == dict_forgotten[num + 1000]:
                    points_ = add_points(points_, True)
                    statistic_forgotten_word_right(word)
                    break
                elif res == 'Выход' or res == 'выход':
                    conn_db.close()
                    print(f'\n\nТренировка завершена!'
                        f'\n>>>> Твой результат ---------> {points_} очков. ')
                    return '============= программа выключена ============='
                elif res == 'Помощь' or res == 'помощь':
                    print(f'----- подсказка: {dict_forgotten[num + 1000]}')
                else:
                    points_ = add_points(points_, False)


def clear_forgotten_table():
    """ """ 
    cur = conn_db.cursor()
    cur.execute("""TRUNCATE TABLE english_words.forgot_en_words 
                RESTART identity""")
    conn_db.commit()
    print('Очистка данный выполнена!')
    return dif_choice()


def insert_new_forgotten_words():
    """ """
    cur = conn_db.cursor()
    cur.execute("""INSERT into english_words.forgot_en_words (word_en, word_ru) 
                SELECT word_en, word_ru 
                FROM english_words.eng_to_rus_words 
                WHERE flag_forgot = 1""")
    conn_db.commit()
    print('Перенос данных выполнен!')
    return dif_choice()


def get_forgotten_dict():
    cur = conn_db.cursor()
    cur.execute("""SELECT id, word_en, word_ru 
                FROM english_words.forgot_en_words""")
    rows = cur.fetchall()
    for row in rows:
        print(f'{row[0]} - {row[1]} - {row[2]}')
    print('\n SELECT is done!')
    return dif_choice()


print(dif_choice())



