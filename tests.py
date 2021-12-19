# -*- coding: utf-8 -*-
import unittest

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

        calls = [
            call(123, "Добро пожаловать, test!\nЯ - <b>bot</b>, бот созданный, чтобы упростить жизнь моего создателя.",
                 parse_mode='html'),
            call(123, "Я могу устанавливать таймеры с нужной для вас информацией", reply_markup=ANY),
            call(123, "Либо открывать сайты нужные для студента ВШЭ.\nДля этого введите команду url")]
        bot_bot.send_message.assert_has_calls(calls)

    @mock.patch('bot.bot')
    def test_settime1(self, bot_bot):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(chat=chat, text='5 сек')
        bot_bot.get_me.return_value = MagicMock(first_name='bot')
        bot.settime(message)
        bot_bot.send_message.assert_called_with(123, 'Введите текст, который вы хотите получить через заданное время')

    @mock.patch('bot.bot')
    def test_settime2(self, bot_bot):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(chat=chat, text='пять сек')
        bot_bot.get_me.return_value = MagicMock(first_name='bot')
        bot.settime(message)
        bot_bot.send_message.assert_called_with(123, 'Вы ввели не численнленное значение времени')

    @mock.patch('bot.bot')
    def test_settime3(self, bot_bot):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(chat=chat, text='пять секунд')
        bot_bot.get_me.return_value = MagicMock(first_name='bot')
        bot.settime(message)
        bot_bot.send_message.assert_called_with(123, 'Вы ввели неверный тип времени')

    @mock.patch('bot.bot')
    def test_choose(self, bot_bot):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(from_user=user, chat=chat)
        bot_bot.get_me.return_value = MagicMock(first_name='bot')
        message.chat.type = "private"
        message.text = "Книги"
        bot.choose(message)

        bot_bot.send_message.assert_called_with(123, "Выбор не велик, но библиотека постоянно пополняется!\n"
                                              "1) И.Сивухин. Основной курс физики\n"
                                              "2) Основы Pyton", reply_markup=ANY)

    @mock.patch('bot.bot')
    def test_choose(self, bot_bot):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(from_user=user, chat=chat)
        bot_bot.get_me.return_value = MagicMock(first_name='bot')
        message.chat.type = "private"
        message.text = "aaa"
        bot.choose(message)
        bot_bot.send_message.assert_called_with(123, "Затрудняюсь ответить")

    @mock.patch('bot.bot')
    def test_settext(self, bot_bot):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(from_user=user, chat=chat)
        bot.users = dict()
        times= {'сек': 5, 'мин': 0, 'час': 0}
        bot_bot.get_me.return_value = MagicMock(first_name='bot')
        bot.settext(message, times)
        bot_bot.send_message.assert_called_with(123, "Через заданное время вам придет заданный текст")

