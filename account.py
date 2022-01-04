import webscraping
import database
import leetcodeapi
from typing import Tuple
from datetime import datetime

class Account:
    def __init__(self, username, total_balance, db: database.Database):
        self.username = username
        self.total_balance = total_balance
        self.db: database.Database = db

    def __str__(self) -> str:
        return f'{self.username} {self.total_balance}'

    def __repr__(self) -> str:
        return f'{self.username} {self.total_balance}'

    def update_username(self, username: str) -> None:
        self.username = username
        self.db.update_username(username)

    def update_balance(self, balance: int) -> None:
        self.total_balance = balance
        self.db.update_user_balance(self.username, balance)

    def get_balance(self) -> int:
        return self.db.get_user_balance(self.username)

    def check_today_submission(self) -> bool:
        return webscraping.check_today_submission(self.username,
                                                  webscraping.RETRY_NUM)

    def check_today_accepted(self) -> int:
        user_profile = leetcodeapi.acquire_user_profile(self.username)
        return leetcodeapi.get_user_solved_problem_count(user_profile)

    def get_accepted_num_and_time(self) -> Tuple[int, str]:
        return self.db.get_accepted_num_and_time(self.username)

    def update_accepted_num_and_time(self, accepted_num: int) -> None:
        self.db.update_accepted_num_and_time(self.username, accepted_num)


if __name__ == '__main__':
    pass
