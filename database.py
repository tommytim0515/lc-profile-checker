import os
import dbm
import time
from constants import *

def open_database(db_name: str) -> any:
    return dbm.open(db_name, 'c')


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = open_database(os.path.join(DATABASE_DIR, db_name))
        self.db[MUTEX_KEY] = '0'

    def __del__(self):
        self.db.close()

    def get_last_update(self):
        return float(self.db[LAST_UPDATE_KEY])

    def mutex_lock(func):
        def wrapper(self, *args, **kwargs):
            while int(self.db[MUTEX_KEY]) == '1':
                time.sleep(0.01)
            self.db[MUTEX_KEY] = '1'
            func(self, *args, **kwargs)
            self.db[MUTEX_KEY] = '0'
        return wrapper

    @mutex_lock
    def update_username(self, username: str, new_name: str) -> None:
        if username not in self.db:
            return
        self.db[new_name] = self.db[username]
        del self.db[username]
        self.db[LAST_UPDATE_KEY] = str(time.time())

    @mutex_lock
    def update_user_balance(self, username: str, balance: int):
        self.db[username] = str(balance)
        self.db[LAST_UPDATE_KEY] = str(time.time())

    def get_user_balance(self, username: str):
        if username not in self.db:
            return None
        return int(self.db[username])


if __name__ == '__main__':
    pass
