import os
import time
import datetime
import glob
import configparser
import console
import curses
import schedule
from typing import List
from datetime import datetime, timedelta
from account import ACCOUNTS, Account
from database import database
from constants import *


def read_config(config_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def parse_config(config_file: str) -> dict:
    config = read_config(config_file)
    return {"usernames": config["USER"]["usernames"]}


def get_usernames(config: dict) -> List:
    return config["usernames"].split(",")


def print_info(func) -> None:
    def wrapper() -> None:
        func()
        for account in ACCOUNTS:
            accepted_num, _ = account.get_accepted_num_and_time()
            print(
                f"{account.username}:\n Balance: "
                f"{account.get_balance()}, Accepted: {accepted_num}"
            )
        print(f"Undistributed: {database().get_undistributed_balance()}")
        print(datetime.now())

    return wrapper


@print_info
def init() -> None:
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    previous_db_files = glob.glob(os.path.join(DATABASE_DIR, "*"))
    for file in previous_db_files:
        os.remove(file)
    configs = parse_config(CONFIG_FILE_DIR)
    usernames = get_usernames(configs)
    for username in usernames:
        ACCOUNTS.append(Account(username, 0, database()))
    for account in ACCOUNTS:
        account.update_balance(0)
        accepted_num = account.check_today_accepted()
        account.update_accepted_num_and_time(accepted_num)


@print_info
def check_everyday_submission() -> None:
    current_undistributed_balance = database().get_undistributed_balance()
    database().update_undistributed_balance(
        current_undistributed_balance + DEPOSIT * len(ACCOUNTS)
    )
    finished_accounts = []
    for account in ACCOUNTS:
        if account.check_today_submission():
            finished_accounts.append(account)
    if len(finished_accounts) <= 0:
        return
    current_undistributed_balance = database().get_undistributed_balance()
    reward_per_account = current_undistributed_balance // len(
        finished_accounts
    )
    for account in finished_accounts:
        account.update_balance(account.get_balance() + reward_per_account)
    database().update_undistributed_balance(
        current_undistributed_balance
        - reward_per_account * len(finished_accounts)
    )


@print_info
def check_everyday_accepted() -> None:
    current_undistributed_balance = database().get_undistributed_balance()
    database().update_undistributed_balance(
        current_undistributed_balance + DEPOSIT * len(ACCOUNTS)
    )
    finished_accounts = []
    for account in ACCOUNTS:
        curr_balance = account.get_balance()
        account.update_balance(curr_balance - DEPOSIT)
        account.update_recent_submission_list()
        accepted_num = account.check_today_accepted()
        prev_ac_num, _ = account.get_accepted_num_and_time()
        if prev_ac_num is None:
            continue
        if accepted_num > prev_ac_num:
            finished_accounts.append(account)
        account.update_accepted_num_and_time(accepted_num)
    if len(finished_accounts) <= 0:
        return
    current_undistributed_balance = database().get_undistributed_balance()
    reward_per_account = current_undistributed_balance // len(
        finished_accounts
    )
    for account in finished_accounts:
        account.update_balance(account.get_balance() + reward_per_account)
    database().update_undistributed_balance(
        current_undistributed_balance
        - reward_per_account * len(finished_accounts)
    )

def check_recent_submissions() -> None:
    for account in ACCOUNTS:
        account.update_recent_submission_list()

def main(stdscr) -> None:
    init()
    console.stdscr_print(stdscr)
    schedule.every().day.at(CHECK_TIME).do(check_everyday_accepted, stdscr)
    schedule.every(5).minutes.do(check_recent_submissions)
    schedule.every(5).seconds.do(console.stdscr_print, stdscr)
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    curses.wrapper(main)
