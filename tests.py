import unittest
import time
from unittest import mock
from unittest.mock import MagicMock, ANY, call
import bot


class TG_test(unittest.TestCase):
    @mock.patch('bot.bot')
    def test_start(self, bot_bot):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(from_user=user, chat=chat)
        bot_bot.get_me.return_value = MagicMock(first_name='bot')
        bot.start_message(message)
        calls = [call(123, "Добро пожаловать, test!\nЯ - <b>bot</b>, бот созданный, чтобы упростить жизнь моего создателя.", parse_mode='html'),
                 call(123, "Я могу устанавливать таймеры с нужной для вас информацией", reply_markup=ANY),
                 call(123, "Либо открывать сайты нужные для студента ВШЭ.\nДля этого введите команду url")]
        bot_bot.send_message.assert_has_calls(calls)

    @mock.patch('bot.bot')
    def test_start(self, bot_bot):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(from_user=user, chat=chat)
        bot_bot.get_me.return_value = MagicMock(first_name='bot')
        bot.start_message(message)
        calls = [
            call(123, "Добро пожаловать, test!\nЯ - <b>bot</b>, бот созданный, чтобы упростить жизнь моего создателя.",
                 parse_mode='html'),
            call(123, "Я могу устанавливать таймеры с нужной для вас информацией", reply_markup=ANY),
            call(123, "Либо открывать сайты нужные для студента ВШЭ.\nДля этого введите команду url")]
        bot_bot.send_message.assert_has_calls(calls)
