from telethon import TelegramClient, sync, events
from telethon.tl.functions.channels import GetMessagesRequest
import unittest
import time




# Your API ID, hash and session string here
api_id = int('12674599')
api_hash = "5750f9474e9b797d9442f442797fbcca"
client = TelegramClient('session_name', api_id, api_hash)


client.start()


class TG_test(unittest.TestCase):
    def testStart(self):
        try:
            client.send_message('@He1per_4u_bot', '/start')
            time.sleep(2)
            messages = client.get_messages('@He1per_4u_bot')
            for message in client.get_messages('@He1per_4u_bot', limit=3):
                m = message.message
            self.assertEqual(len(messages), 1)
            text = f'Добро пожаловать'
            self.assertRegex(m, text)
        except:
            self.assertFalse(True)

    def testurl(self):
        try:
            client.send_message('@He1per_4u_bot', '/url')
            time.sleep(2)
            messages = client.get_messages('@He1per_4u_bot')
            for message in client.get_messages('@He1per_4u_bot', limit=1):
                m = message.message
            self.assertEqual(len(messages), 1)
            text = f'Выберите сайт, на который вы хотите перейти'
            self.assertRegex(m, text)
        except:
            self.assertFalse(True)

    def testurl2(self):
        try:
            client.send_message('@He1per_4u_bot', '/Url')
            time.sleep(2)
            messages = client.get_messages('@He1per_4u_bot')
            for message in client.get_messages('@He1per_4u_bot', limit=1):
                m = message.message
            self.assertEqual(len(messages), 1)
            text = f'Выберите сайт, на который вы хотите перейти'
            self.assertRegex(m, text)
        except:
            self.assertFalse(True)

    def testurl3(self):
        try:
            client.send_message('@He1per_4u_bot', '/u')
            time.sleep(2)
            messages = client.get_messages('@He1per_4u_bot')
            for message in client.get_messages('@He1per_4u_bot', limit=1):
                m = message.message
            self.assertEqual(len(messages), 1)
            text = f'Выберите сайт, на который вы хотите перейти'
            self.assertRegex(m, text)
        except:
            self.assertFalse(True)





















