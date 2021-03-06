import os
import dbm
import time
from constants import *
from datetime import datetime
from typing import Any, Callable, Tuple, Optional

DATABASE = None

def database():
    global DATABASE
    if DATABASE is None:
        DATABASE = Database(DATABASE_NAME)
    return DATABASE

def open_database(db_name: str) -> Any:
    return dbm.open(db_name, "c")


class Database:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.db = open_database(os.path.join(DATABASE_DIR, db_name))
        self.db[MUTEX_KEY] = "0"

    def __del__(self) -> None:
        self.db.close()

    def get_last_update(self) -> float:
        return float(self.db[LAST_UPDATE_KEY])

    def mutex_lock(func: Any) -> Callable:
        def wrapper(self, *args, **kwargs):
            while int(self.db[MUTEX_KEY]) == "1":
                time.sleep(0.01)
            self.db[MUTEX_KEY] = "1"
            func(self, *args, **kwargs)
            self.db[MUTEX_KEY] = "0"

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
        key = BALANCE_PREFIX + username
        self.db[key] = str(balance)
        self.db[LAST_UPDATE_KEY] = str(time.time())

    def get_user_balance(self, username: str):
        key = BALANCE_PREFIX + username
        if key not in self.db:
            return None
        return int(self.db[key])

    @mutex_lock
    def update_undistributed_balance(self, amount: int) -> None:
        self.db[UNDISTRIBUTED_KEY] = str(amount)
        self.db[LAST_UPDATE_KEY] = str(time.time())

    def get_undistributed_balance(self) -> int:
        if UNDISTRIBUTED_KEY not in self.db:
            self.db[UNDISTRIBUTED_KEY] = "0"
            self.db[LAST_UPDATE_KEY] = str(time.time())
            return 0
        return int(self.db[UNDISTRIBUTED_KEY])

    @mutex_lock
    def update_accepted_num_and_time(
        self, username: str, accepted_num: int
    ) -> None:
        key = ACCEPTED_PREFIX + username
        self.db[key] = (
            str(accepted_num) + " " + datetime.now().strftime(DATETIME_FORMAT)
        )
        self.db[LAST_UPDATE_KEY] = str(time.time())

    def get_accepted_num_and_time(
        self, username: str
    ) -> Tuple[Optional[int], Optional[str]]:
        key = ACCEPTED_PREFIX + username
        if key not in self.db:
            return None, None
        accepted_num, time_str = self.db[key].decode().split(" ")
        return int(accepted_num), time_str


if __name__ == "__main__":
    pass
