import sqlite3

class BotDB:
    con = sqlite3.connect('')
    cursor = con.cursor()
    with con:
        def add_user(self, user_id):
            self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

        def user_exists(self, user_id):
            result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
            return bool(len(result.fetchall()))