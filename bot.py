import telebot
import threading
import datetime
import sqlite3
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start_message(message):

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
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button1 = telebot.types.InlineKeyboardButton(text="Расписание", url="https://ruz.hse.ru/ruz/main")
    url_button2 = telebot.types.InlineKeyboardButton(text="Библиотека", url="https://library.hse.ru/")
    url_button3 = telebot.types.InlineKeyboardButton(text="Smart LMS", url="https://smartedu.hse.ru/login?target=/")
    keyboard.add(url_button1, url_button2, url_button3)
    bot.send_message(message.chat.id,
                     'Выберите сайт, на который вы хотите перейти', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda x: x.data == "set timer")
def presettimer(query):
    message = query.message
    bot.send_message(message.chat.id, "Введите один из пресетов таймера:\n"
                     "1: n сек\n"
                     "2: n мин\n"
                     "3: n час")
    bot.register_next_step_handler(message, settime)
def settime(message):
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
    bot.send_message(message.chat.id,
                     'Введите текст, который вы хотите получить через заданное время')
    bot.register_next_step_handler(message, settext, times)

def settext(message, times):
    cur_date = datetime.datetime.now()
    izmdate = datetime.timedelta(days=0, hours=times['час'], minutes=times['мин'], seconds=times['сек'])
    cur_date += izmdate
    users[message.chat.id] = (cur_date, message.text)
    bot.send_message(message.chat.id,
                     'Через заданное время вам придет заданный текст')

def check_date():
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
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("Установить таймер", callback_data='set timer')
    keyboard.add(button)
    return keyboard

if __name__ == "__main__":
    users = {}
    while True:
        try:
            bot.polling(non_stop=True)
            check_date()
        except:
            print("Что-то сломалось")
