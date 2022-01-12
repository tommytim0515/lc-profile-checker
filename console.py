import time
from datetime import datetime
from account import *
from database import database
from constants import *


def print_date(stdscr) -> None:
    stdscr.addstr("=" * CONSOLE_TOTAL_LENGTH + "\n")
    today_date = datetime.now().strftime(DATETIME_FORMAT)
    stdscr.addstr(f"| {today_date:<{CONSOLE_TOTAL_LENGTH-3}}|\n")


def print_user_profile(stdscr, ac: Account) -> None:
    stdscr.addstr("=" * CONSOLE_TOTAL_LENGTH + "\n")
    stdscr.addstr(
        f"| User: {ac.username:<{CONSOLE_USERNAME_LENGTH}}| "
        f"Balance: {ac.total_balance:<{CONSOLE_BALANCE_LENGTH}}|\n"
    )
    if len(ac.recent_submission_list) > 0:
        stdscr.addstr("-" * CONSOLE_TOTAL_LENGTH + "\n")
        stdscr.addstr(
            "| Recent Accepted Submissions:"
            + " " * (CONSOLE_TOTAL_LENGTH - 31)
            + "|\n"
        )
        for submission in ac.recent_submission_list:
            stdscr.addstr("-" * CONSOLE_TOTAL_LENGTH + "\n")
            problem_description = f"{submission[0]} ({submission[1]})"
            for i in range(
                0, len(problem_description), CONSOLE_TOTAL_LENGTH - 3
            ):
                stdscr.addstr(
                    f"| {problem_description[i:i+CONSOLE_TOTAL_LENGTH-3]:<{CONSOLE_TOTAL_LENGTH-3}}|\n"
                )


def print_total_accepted_num(stdscr, ac: Account) -> None:
    stdscr.addstr("-" * CONSOLE_TOTAL_LENGTH + "\n")
    stdscr.addstr(
        f"| Total Accepted: {ac.accepted_num:<{CONSOLE_TOTAL_LENGTH-19}}|\n"
    )


def print_undistributed_balance(stdscr) -> None:
    stdscr.addstr("=" * CONSOLE_TOTAL_LENGTH + "\n")
    stdscr.addstr(
        f"| Undistributed Balance: {database().get_undistributed_balance():<{CONSOLE_TOTAL_LENGTH-26}}|\n"
    )


def print_endline(stdscr) -> None:
    stdscr.addstr("=" * CONSOLE_TOTAL_LENGTH + "\n")

def stdscr_print(stdscr) -> None:
    stdscr.clear()
    print_date(stdscr)
    for account in ACCOUNTS:
        print_user_profile(stdscr, account)
        print_total_accepted_num(stdscr, account)
    print_undistributed_balance(stdscr)
    print_endline(stdscr)
    stdscr.refresh()


if __name__ == "__main__":
    pass
