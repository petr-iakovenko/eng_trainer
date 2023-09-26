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
cursor.execute("select word_en, countet_try, counter_forgot from english_words.eng_to_rus_words where flag_forgot = 1 order by counter_forgot desc limit 100;")
rows = cursor.fetchall()
print('==============================================================')
print('Статистика:')
# print(*rows, sep='\n')
print(f'Слово/Фраза - Удачных попыток - Вызов помощи')
for row in rows:
    print(f'"{row[0]}" - {row[1]} - {row[2]}')
print('==============================================================')


def add_word_db_en(word):
    """to update word on eng"""
    list_ = []
    cur = conn_db.cursor()
    cur.execute("""SELECT word_en FROM english_words.eng_to_rus_words WHERE word_en = %s""", (word,))
    row = cur.fetchall()
    if row == list_:
        cur.execute("""insert into english_words.eng_to_rus_words (word_en) VALUES (%s)""", (word,))
        conn_db.commit()
    else:
        pass

def add_translate_word_db_en(word, translate):
    """to update translate word on rus"""
    cur = conn_db.cursor()
    cur.execute("""update english_words.eng_to_rus_words set word_ru = %s WHERE word_en = %s """, (translate, word,))
    conn_db.commit()

def add_word_db_ru(word):
    """добавляет в БД слова RU"""
    list_ = []
    cur = conn_db.cursor()
    cur.execute("""SELECT word FROM russian_words.words WHERE word = %s""", (word,))
    row = cur.fetchall()
    if row == list_:
        cur.execute("""insert into russian_words.words (word) VALUES (%s)""", (word,))
        conn_db.commit()
    else:
        pass

def statistic_word_right(word):
    """to update counter correct response"""
    cur = conn_db.cursor()
    cur.execute("""UPDATE english_words.eng_to_rus_words  SET countet_try = countet_try + 1 WHERE word_en = %s""", (word,))
    conn_db.commit()
    cur.execute("""SELECT countet_try FROM english_words.eng_to_rus_words WHERE word_en = %s""", (word,))
    rows = cur.fetchall()
    if rows[0][0] == 10:
        cur.execute("""UPDATE english_words.eng_to_rus_words  SET flag_forgot = 0 WHERE word_en = %s""", (word,))
        conn_db.commit()


def statistic_word_help(word):
    """to update counter run 'помощь'"""
    cur = conn_db.cursor()
    cur.execute("""UPDATE english_words.eng_to_rus_words  SET countet_try = 0 WHERE word_en = %s""", (word,))
    conn_db.commit()
    cur.execute("""UPDATE english_words.eng_to_rus_words  SET counter_forgot = counter_forgot + 1 WHERE word_en = %s""", (word,))
    conn_db.commit()
    

def flag_forgot(word): 
    cur = conn_db.cursor()
    cur.execute("""UPDATE english_words.eng_to_rus_words  SET flag_forgot = 1 WHERE word_en = %s""", (word,))
    conn_db.commit()


def add_points(points_, flag):
    """to update counter points"""
    if flag == True:
        points_ += 1
        print('>>>> ВЕРНО! +1 point.')
    else:
        print('>>>> ВЫ ОШИБЛИСЬ! -5 points')
        points_ -= 5
        print(f'\n==================================================\n>>>> СЧЕТ: {points_} points.')
        print('Попробуй еще раз! \n(чтобы показать ответ набери "помощь")!\n==================================================')
    if points_ % 10 == 0:
        print(f'>>>> Твой результат ---------> {points_} очков.')
    elif points_ == 21:
        print(f'Поздравляю!\nТвой результат {points_} очков\nПоменяй сложность если слишком легко.')
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
    19: 'Do you hear?', 1019: 'слышите?',
    20: 'Take a look', 1020: 'взгляни',
    21: 'Arrive', 1021: 'прибывать',
    22: 'Depart', 1022: 'покидать',
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
    44: 'To assure', 1044: 'убеждать',
    45: 'To avoid', 1045: 'избегать',
    46: 'To receive', 1046: 'получать',
    47: 'To remain', 1047: 'напоминать',
    48: 'To retain', 1048: 'удержать',
    49: 'To obtain', 1049: 'получить; добиться',
    50: 'To waste', 1050: 'тратить впустую',
    51: 'To prefer', 1051: 'предпочитать',
    52: 'To explain', 1052: 'объяснять',
    53: 'Latency', 1053: 'задержка',
    54: 'Subquery', 1054: 'подзапрос',
    55: 'Additional', 1055: 'дополнительный',
    56: 'Enroll', 1056: 'поступить',
    57: 'Attempt', 1057: 'попытка',
    58: 'Precision', 1058: 'точность',
    59: 'confident', 1059: 'уверенный',
    60: 'environment', 1060: 'окружающая среда обстановка',
    61: 'impress', 1061: 'впечатлить',
    62: "Let's continue", 1062: 'продолжим',
    63: 'Prove', 1063: 'докажи',
    64: 'Essential', 1064: 'важный',
    65: 'Carry out', 1065: 'выполнять',
    66: 'Can you handle it?', 1066: 'справишься?',
    67: 'Pressure', 1067: 'давление',
    68: 'Take action', 1068: 'принять решение',
    69: 'Provide', 1069: 'предусматривать',
    70: 'I believe', 1070: 'верю',
    71: 'Mention', 1071: 'упоминание',
    72: 'Match', 1072: 'соответствовать',
    73: 'Solve', 1073: 'решить(проблему)',
    74: 'Contribute', 1074: 'делать вклад',
    75: 'Rest', 1075: 'отдых',
    76: 'Hold it', 1076: 'подержи',
    77: 'Not for long', 1077: 'ненадолго',
    78: 'Foreign', 1078: 'зарубежный',
    79: 'Abroad', 1079: 'за границей',
    80: 'Collaborate', 1080: 'сотрудничать',
    81: 'Upstairs', 1081: 'наверху',
    82: 'Jointly', 1082: 'совместно',
    83: 'Produce', 1083: 'производить',
    84: 'Design', 1084: 'намерение',
    85: 'Succeed', 1085: 'добиться успеха',
    86: 'Hire', 1086: 'нанимать',
    87: 'Determine', 1087: 'определять',
    88: 'Cool down', 1088: 'остынь',
    89: 'Wage', 1089: 'заработная плата',
    90: 'Refer to', 1090: 'ссылаться на',
    91: 'Brief', 1091: 'краткий',
    92: 'Quality', 1092: 'качество',
    93: 'State', 1093: 'состояние',
    94: 'Lack', 1094: 'недостаток; отсутствие',
    95: 'Сontinuous', 1095: 'непрерывный',
    96: 'Ahead', 1096: 'впереди',
    97: 'Seek', 1097: 'искать',
    98: 'Advice', 1098: 'совет; рекомендация',
    99: 'Stand out', 1099: 'выделяться',
    100: 'Do you feel it?', 1100: 'чувствуешь?',
    101: 'Honest', 1101: 'честный; подленный',
    102: 'Relate', 1102: 'устанавливать связь между',
    103: 'Direct', 1103: 'направлять',
    104: 'Slight', 1104: 'легкий',
    105: 'Similar', 1105: 'похожий',
    106: 'Whole', 1106: 'целое',
    107: 'Enjoy', 1107: 'наслаждайся',
    108: 'Give up on trying', 1108: 'отказаться от попыток',
    109: 'Passionate about', 1109: 'увлечен',
    110: 'Include', 1110: 'содержит',
    111: 'Jealousy', 1111: 'ревность; зависть',
    112: 'Overall', 1112: 'общий; в целом',
    113: 'Loud', 1113: 'громкий',
    114: 'Can you imagine?', 1114: 'представляешь?',
    115: 'Handle setbacks', 1115: 'справляться с неудачами',
    116: 'I confirm', 1116: 'подтверждаю',
    117: "Let's get started", 1117: 'приступим',
    118: 'Sign in', 1118: 'войдите',
    119: 'Capable', 1119: 'способный',
    120: 'Let me go', 1120: 'пусти',
    121: 'Huge disaster', 1121: 'огромная катастрофа',
    122: 'Able', 1122: 'способный',
    123: 'Self-awareness', 1123: 'самосознание',
    124: 'Improve', 1124: 'улучшать',
    125: 'Outcome', 1125: 'результат',
    126: 'Prevent', 1126: 'предотвратить',
    127: 'Actions', 1127: 'действие',
    128: 'Have a seat', 1128: 'присаживайся',
    129: 'Blame', 1129: 'винить',
    130: 'Respond', 1130: 'отвечать реагировать',
    131: 'Admitting', 1131: 'признание',
    132: 'Shortcoming', 1132: 'недостаток',
    133: 'Humble', 1133: 'скромный',
    134: 'Validating', 1134: 'проверка',
    135: 'Willing', 1135: 'готовый',
    136: 'That', 1136: 'что',
    137: 'Overcome', 1137: 'преодолеть',
    138: 'Regarding', 1138: 'относительно',
    139: 'Above', 1139: 'вышесказанный',
    140: 'Impressed', 1140: 'впечатлен',
    141: 'Could be', 1141: 'может быть',
    142: 'Fit for', 1142: 'подходит для',
    143: 'Represents', 1143: 'представляет(описание)',
    144: 'Leading', 1144: 'ведущий, передовой',
    145: 'Revenue', 1145: 'доход',
    146: 'Available', 1146: 'доступный',
    147: 'Improving', 1147: 'улучшение',
    148: 'Validating', 1148: 'проверка',
    149: 'Expanding', 1149: 'расширение',
    150: 'Apart', 1150: 'отдельно',
    151: 'Confirming', 1151: 'подтверждающий',
    152: 'Provider', 1152: 'поставщик',
    153: 'Collecting', 1153: 'сбор',
    154: 'Set', 1154: 'набор',
    155: 'Explain', 1155: 'объяснять',
    156: 'What did you mean?', 1156: 'Что ты имел ввиду?',
    157: 'He is bored', 1157: 'он утомленный',
    158: 'Where it does hurt?', 1158: 'Где болит?',
    159: 'It got cold', 1159: 'похолодало',
    160: 'Hurt', 1160: 'больно',
    161: "I'm looking at", 1161: 'я смотрю на',
    162: "I'm looking after", 1162: 'я присматриваю за',
    163: "I'm looking for", 1163: 'я ищу',
    164: "I'm waiting for my friend", 1164: 'жду своего друга',
    165: 'fast faster fastest', 1165: 'быстрый быстрее самый быстрый',
    166: 'Better', 1166: 'лучший',
    167: 'Well', 1167: 'хорошо',
    168: 'It takes time', 1168: 'это занимает время',
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
    185: 'Good at', 1185: 'хорош в',
    186: 'Advance', 1186: 'продвигаться',
    187: 'To set goal', 1187: 'устанавливать цель',
    188: 'Few / several', 1188: 'несколько',
    189: 'On a call', 1189: 'на переговорах',
    190: 'Point out', 1190: 'указать',
    191: 'Since then', 1191: 'с того времени',
    192: 'Neglect', 1192: 'пренебрегать',
    193: 'Resolve', 1193: 'решить',
    194: 'Growth', 1194: 'рост',
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
    print('\n\n============= программа "Тренажер английского v2.0" запущена =============\n\n')
    while True:
        print('Выбери сложность:\nTranslate B1 words to RUS:\n\t1 - All words\nTranslate B1 forgotten_words to RUS:\n\t2 - All words')
        difficulty = (input('Выбрана сложность: ').strip())
        if difficulty == '1':
            print('\n"Translate B1 words to RUS"')
            print(
                '- переводите фразы на англиский язык; \n- за правильный ответ ты получишь +1 point и -5 points если ошибешься.')
            return diff_1()
        elif difficulty == '2':
            print('\n"Translate B1 forgotten_words to RUS"')
            print(
                '- переводите фразы на англиский язык; \n- за правильный ответ ты получишь +1 point и -5 points если ошибешься.')
            return diff_2()
        else:
            print('ОШИБКА ВВОДА!\n \n \n')
    

def diff_1():
    points_ = 0
    while True:
        num = random.randint(1, 137)
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
                print(f'\n\nТренировка завершена!\n>>>> Твой результат ---------> {points_} очков. ')
                return '============= программа выключена =============\n\n'
            elif res == 'Помощь' or res == 'помощь':
                print(f'----- подсказка: {dict_pol_les_preply[num + 1000]}')
                statistic_word_help(word)
                flag_forgot(word)
            else:
                points_ = add_points(points_, False)

def diff_2():
    points_ = 0
    while True:
        num = random.randint(1001, 1137) # 1137
        while True:
            print(f'\nRu: {dict_pol_les_preply[num]}')
            res = input('En: ').strip()
            if res == dict_pol_les_preply[num - 1000]:
                points_ += points(True)
                print('>>>> ВЕРНО! +1 point.')
                if points_ % 10 == 0:
                    print(f'>>>> Твой результат ---------> {points_} очков.')
                elif points_ == 21:
                    print(f'Поздравляю!\nТвой результат {points_} очков\nПоменяй сложность если слишком легко.')
                break
            elif res == 'Exit' or res == 'exit':
                print(f'\n\nТренировка завершена!\n>>>> Твой результат ---------> {points_} очков. ')
                return '============= программа выключена =============\n\n'
            elif res == 'Help' or res == 'help':
                print(f'----- подсказка: {dict_pol_les_preply[num - 1000]}')
            else:
                print('>>>> ВЫ ОШИБЛИСЬ! -5 points')
                points_ -= points(False)
                print(f'\n==================================================\n>>>> СЧЕТ: {points_} points.')
                print('Попробуй еще раз! \n(чтобы показать ответ набери "help")!\n==================================================')


print(dif_choice())


