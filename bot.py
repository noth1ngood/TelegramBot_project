import telebot
import threading
import datetime
import xlrd
import sqlite3 as lite
from config import TOKEN
from database import BotDB
bot = telebot.TeleBot(TOKEN)
conn = lite.connect("Users.db", check_same_thread=False)
cursor = conn.cursor()
"""функция добавляющая данные пользователя в таблицу test"""
def dbtableval(user_id: int, user_name: str, user_surname: str, username: str):
    """

    :param user_id: id пользователя
    :param user_name: имя пользователя
    :param user_surname: фамилия пользователя
    :param username: ник пользователя
    :return: добавляет данные пользователя в таблицу test, которая находится в Users.db
    """
    cursor.execute('INSERT INTO test (user_id, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
    conn.commit()
    print("данные добавлены")
"""раздел, обрабатывающий команду Start"""
@bot.message_handler(commands=['start'])
def start_message(message): #функция, обрабатывающая команду start

    """
    :param message: принимает
    :return: три сообщения с прикреппленной кнопкой
    """

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный, чтобы упростить жизнь моего создателя.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.send_message(message.chat.id,
                     "Я могу устанавливать таймеры с нужной для вас информацией",
                     reply_markup=get_keyboard())
    bot.send_message(message.chat.id,
                     "Либо открывать сайты нужные для студента ВШЭ.\nДля этого введите команду url")
'''@bot.message_handler(content_types=['text'])
def getnote(message):
    """

    :param message: принимает на вход сообщение пользователя
    :return: сообщение
    """
    if message.text.lower() == "запиши":
        bot.send_message(message.from_user.id, "{0.first_name}!\n Я записал ваши данные в базу данных".format(
            message.from_user, bot.get_me(), parse_mode='html'))

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_surname = message.from_user.last_name
        username = message.from_user.username

        dbtableval(user_id=us_id, user_name=us_name, user_surname=us_surname, username=username)
        '''
@bot.message_handler(commands=['books', 'Books', 'notes', 'Notes'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton("Вывести заметки из Exel")
    button2 = telebot.types.KeyboardButton("Книги")
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "Выбирай, {0.first_name}\n".format(message.from_user),parse_mode='html', reply_markup=keyboard)
@bot.message_handler(func=lambda message: True)
def choose(message):
    if message.chat.type == "private":
        if message.text == "Вывести заметки из Exel":
            notes = xlrd.open_workbook('Notes.xls', formatting_info=True)
            list = notes.sheet_by_index(0)
            row = list.row_values(0)
            bot.send_message(message.chat.id, row)
        elif message.text == "Книги":
            bot.send_message(message.chat.id, "не доделано")
        else:
            bot.send_message(message.chat.id, "Затрудняюсь ответить")
@bot.message_handler(commands=['url', 'Url', 'u'])
def url(message):
    """

    :param message: сообщение
    :return: три кнопки, привязпнные к сообщению
    """
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    url_button1 = telebot.types.InlineKeyboardButton(text="Расписание", url="https://ruz.hse.ru/ruz/main")
    url_button2 = telebot.types.InlineKeyboardButton(text="Библиотека", url="https://library.hse.ru/")
    url_button3 = telebot.types.InlineKeyboardButton(text="Smart LMS", url="https://smartedu.hse.ru/login?target=/")
    keyboard.add(url_button1, url_button2, url_button3)
    bot.send_message(message.chat.id,
                     'Выберите сайт, на который вы хотите перейти', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda x: x.data == "set timer")
def presettimer(query):
    """

    :param query: запрос на установление таймера-напоминалки
    :return:
    """
    message = query.message
    bot.send_message(message.chat.id, "Введите один из пресетов таймера:\n"
                     "1: n сек\n"
                     "2: n мин\n"
                     "3: n час")
    bot.register_next_step_handler(message, settime)
def settime(message):
    """

    :param message: данные, которые отображают время на которое устанавливается уведомление
    :return:
    """
    times = {
        'сек': 0,
        'мин': 0,
        'час': 0
    }
    quantity, type_time = message.text.split()
    if type_time not in times.keys():
        bot.send_message(message.chat.id,
                         'Вы ввели неверный тип времени')

    if not quantity.isdigit():
        bot.send_message(message.chat.id,
                         'Вы ввели не численнленное значение времени')
    times[type_time] = int(quantity)
    presettext(message, times)

def presettext(message, times):
    """

    :param message: данные, по которым устанавливается таймер
    :param times: численное значение времени в секундах, на которое ставится таймер
    :return:
    """
    bot.send_message(message.chat.id,
                     'Введите текст, который вы хотите получить через заданное время')
    bot.register_next_step_handler(message, settext, times)

def settext(message, times):
    """

    :param message: данные, по которым ставится будильник
    :param times: численное значение таймера
    :return: сообщение об успешном установлении таймера
    """
    cur_date = datetime.datetime.now()
    izmdate = datetime.timedelta(days=0, hours=times['час'], minutes=times['мин'], seconds=times['сек'])
    cur_date += izmdate
    users[message.chat.id] = (cur_date, message.text)
    bot.send_message(message.chat.id,
                     'Через заданное время вам придет заданный текст')

def check_date():
    """

    :return: напоминание с указанным текстом
    """
    nowdate = datetime.datetime.now()
    delusers = []
    for chat_id, value in users.items():
        timer = value[0]
        message = value[1]
        if nowdate >= timer:
            bot.send_message(chat_id, "Ваше напоминание: \n" + message)
            delusers.append(chat_id)
    for user in delusers:
        del users[user]
    threading.Timer(1, check_date).start()

def get_keyboard():
    """

    :return: возвращает клавиатуру
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("Установить таймер", callback_data='set timer')
    keyboard.add(button)
    return keyboard

if __name__ == "__main__":
    users = {}
    while True:
        try:
            bot.polling(non_stop=True, interval=0)
            check_date()
        except:
            print("Что-то сломалось")
