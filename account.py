import webscraping
import database


class Account:
    def __init__(self, username, total_balance, db: database.Database):
        self.username = username
        self.total_balance = total_balance
        self.db: database.Database = db

    def __str__(self):
        return f'{self.username} {self.total_balance}'

    def __repr__(self):
        return f'{self.username} {self.total_balance}'

    def update_username(self, username):
        self.username = username
        self.db.update_username(username)

    def update_balance(self, balance):
        self.total_balance = balance
        self.db.update_user_balance(self.username, balance)

    def get_balance(self):
        return self.db.get_user_balance(self.username)

    def check_today_submission(self):
        return webscraping.check_today_submission(self.username,
                                                  webscraping.RETRY_NUM)


if __name__ == '__main__':
    pass
