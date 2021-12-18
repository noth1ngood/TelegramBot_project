import telebot
import threading
import datetime
import xlrd
from config import TOKEN
bot = telebot.TeleBot(TOKEN)
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
    kolvo, type_time = message.text.split()
    if type_time not in times.keys():
        bot.send_message(message.chat.id,
                         'Вы ввели неверный тип времени')

    if not kolvo.isdigit():
        bot.send_message(message.chat.id,
                         'Вы ввели не численнленное значение времени')
    times[type_time] = int(kolvo)

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
@bot.message_handler(commands=['books', 'Books', 'notes', 'Notes'])
def send_welcome(message):
    '''

    :param message: команда, которая запускает данную функцию
    :return: клавиатуру, с двумя кнопками
    '''
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton("Вывести заметки из Exel")
    button2 = telebot.types.KeyboardButton("Книги")
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "Выбирай, {0.first_name}\n".format(message.from_user),parse_mode='html', reply_markup=keyboard)
@bot.message_handler(func=lambda message: True)
def choose(message):
    """

    :param message: на вход идет либо "книги", либо "вывести заметки из Exel"
    :return: выводит либо содержимое таблицы Exel, либо список книг
    """
    if message.chat.type == "private":
        if message.text == "Вывести заметки из Exel":
            notes = xlrd.open_workbook('Notes.xls', formatting_info=True)
            list = notes.sheet_by_index(0)
            for i in range(list.nrows):
                row = list.row_values(i)
                bot.send_message(message.chat.id, row)
        elif message.text == "Книги":
            bot.send_message(message.chat.id, "Выбор не велик, но библиотека постоянно пополняется!\n"
                                              "И.Сивухин. Основной курс физики\n"
                                              "Акулов. Курс по информатике")
        else:
            bot.send_message(message.chat.id, "Затрудняюсь ответить")
if __name__ == "__main__":
    users = {}
    while True:
        try:
            bot.polling(non_stop=True, interval=0)
            check_date()
        except:
            print("Что-то сломалось")
