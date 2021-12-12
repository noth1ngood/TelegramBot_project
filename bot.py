import telebot
import threading
import datetime
from config import TOKEN
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, я бот умеющий делать напоминания!', reply_markup=get_keyboard())
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
                     'Введите текст, который вы хотите получить через данное время')
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
            bot.send_message(chat_id, message)
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
            bot.polling()
            check_date()
        except:
            print("Что-то сломалось")
