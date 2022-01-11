import os
import glob
import schedule
import account as ac
import configparser
import database
from constants import *
from typing import List
from datetime import datetime


ACCOUNTS = []
DATABASE = None


def read_config(config_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def parse_config(config_file: str) -> dict:
    config = read_config(config_file)
    return {
        "usernames": config["USER"]["usernames"],
    }


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
        if DATABASE is None:
            return
        print(f"Undistributed: {DATABASE.get_undistributed_balance()}")
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
    global DATABASE
    DATABASE = database.Database(DATABASE_NAME)
    for username in usernames:
        ACCOUNTS.append(ac.Account(username, 0, DATABASE))
    for account in ACCOUNTS:
        account.update_balance(0)
        accepted_num = account.check_today_accepted()
        account.update_accepted_num_and_time(accepted_num)


@print_info
def check_everyday_submission() -> None:
    if DATABASE is None:
        return
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    DATABASE.update_undistributed_balance(
        current_undistributed_balance + DEPOSIT * len(ACCOUNTS)
    )
    finished_accounts = []
    for account in ACCOUNTS:
        if account.check_today_submission():
            finished_accounts.append(account)
    if len(finished_accounts) <= 0:
        return
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    reward_per_account = current_undistributed_balance // len(
        finished_accounts
    )
    for account in finished_accounts:
        account.update_balance(account.get_balance() + reward_per_account)
    DATABASE.update_undistributed_balance(
        current_undistributed_balance
        - reward_per_account * len(finished_accounts)
    )


@print_info
def check_everyday_accepted() -> None:
    if DATABASE is None:
        return
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    DATABASE.update_undistributed_balance(
        current_undistributed_balance + DEPOSIT * len(ACCOUNTS)
    )
    finished_accounts = []
    for account in ACCOUNTS:
        curr_balance = account.get_balance()
        account.update_balance(curr_balance - DEPOSIT)
        accepted_num = account.check_today_accepted()
        prev_ac_num, _ = account.get_accepted_num_and_time()
        if prev_ac_num is None:
            continue
        if accepted_num > prev_ac_num:
            finished_accounts.append(account)
        account.update_accepted_num_and_time(accepted_num)
    if len(finished_accounts) <= 0:
        return
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    reward_per_account = current_undistributed_balance // len(
        finished_accounts
    )
    for account in finished_accounts:
        account.update_balance(account.get_balance() + reward_per_account)
    DATABASE.update_undistributed_balance(
        current_undistributed_balance
        - reward_per_account * len(finished_accounts)
    )


def main() -> None:
    init()
    if DATABASE is None:
        print("Database not initialized.")
        return
    # check_everyday_submission()
    # check_everyday_accepted()
    schedule.every().day.at(CHECK_TIME).do(check_everyday_accepted)
    # schedule.every(5).minutes.do(check_everyday_submission)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
