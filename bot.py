import telebot
from config import TOKEN
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, я бот умеющий делать напоминания!', reply_markup=get_keyboard())
@bot.callback_query_handler(func=lambda x: x.date == "set timer")
def presettimer(query):
    message = query.message
    bot.send_message(message.chat.id, "Введите один из пресетов таймера:\n"
                     "1: n сек\n"
                     "2: n мин\n"
                     "3: n час")
    bot.register_next_step_handler(message, settime)
def settime(message):
    pass


def get_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("Установить таймер", callback_data='set timer')
    keyboard.add(button)
    return keyboard

if __name__ == "__main__":
    while True:
        try:
            bot.polling()
        except:
            print("Что-то сломалось")
