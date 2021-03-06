import database
import leetcodeapi
from typing import Tuple, Optional, List
from constants import ENABLE_WEB_SCRAPING


class Account:
    def __init__(self, username, total_balance, db: database.Database):
        self.username = username
        self.total_balance = total_balance
        self.accepted_num = 0
        self.recent_submission_list = []
        self._db: database.Database = db

    def __str__(self) -> str:
        return f"{self.username} {self.total_balance}"

    def __repr__(self) -> str:
        return f"{self.username} {self.total_balance}"

    def update_username(self, username: str) -> None:
        self.username = username
        self._db.update_username(username)

    def update_balance(self, balance: int) -> None:
        self.total_balance = balance
        self._db.update_user_balance(self.username, balance)

    def get_balance(self) -> int:
        return self._db.get_user_balance(self.username)

    def check_today_submission(self) -> bool:
        if ENABLE_WEB_SCRAPING:
            import webscraping

            return webscraping.check_today_submission(
                self.username, webscraping.RETRY_NUM
            )
        return False

    def check_today_accepted(self) -> int:
        session, headers = leetcodeapi.make_session(self.username)
        user_profile = leetcodeapi.acquire_user_profile(session, headers, self.username)
        return leetcodeapi.get_user_solved_problem_count(user_profile)

    def get_accepted_num_and_time(self) -> Tuple[Optional[int], Optional[str]]:
        return self._db.get_accepted_num_and_time(self.username)

    def update_accepted_num_and_time(self, accepted_num: int) -> None:
        self.accepted_num = accepted_num
        self._db.update_accepted_num_and_time(self.username, accepted_num)

    def update_recent_submission_list(self) -> None:
        session, headers = leetcodeapi.make_session(self.username)
        recent_submissions = leetcodeapi.acquire_recent_submission_list(
            session, headers, self.username
        )
        self.recent_submission_list = leetcodeapi.get_yesterday_accepted_submissions(
            recent_submissions
        )


ACCOUNTS: List[Account] = []

if __name__ == "__main__":
    pass
