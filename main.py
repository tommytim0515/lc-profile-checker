import os
import time
import glob
import schedule
import account as ac
import configparser
import database
from constants import *
from typing import List


ACCOUNTS = []
DATABASE = None


def read_config(config_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def parse_config(config_file: str) -> dict:
    config = read_config(config_file)
    return {
        'usernames': config['USER']['usernames'],
    }


def get_usernames(config: dict) -> List:
    return config['usernames'].split(',')


def init():
    previous_db_files = glob.glob(os.path.join(DATABASE_DIR, '*'))
    for file in previous_db_files:
        os.remove(file)
    configs = parse_config(CONFIG_FILE_DIR)
    usernames = get_usernames(configs)
    DATABASE = database.Database(DATABASE_NAME)
    for username in usernames:
        ACCOUNTS.append(ac.Account(username, 0, DATABASE))
    for account in ACCOUNTS:
        account.update_balance(0)


def check_everyday_submission():
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    DATABASE.update_undistributed_balance(
        current_undistributed_balance + DEPOSIT * len(ACCOUNTS))
    finished_accounts = []
    for account in ACCOUNTS:
        if account.check_today_submission():
            finished_accounts.append(account)
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    reward_per_account = current_undistributed_balance // len(
        finished_accounts)
    for account in finished_accounts:
        account.update_balance(account.get_balance() + reward_per_account)
    DATABASE.update_undistributed_balance(
        current_undistributed_balance - reward_per_account * len(finished_accounts))


def main():
    init()
    schedule.every().day.at(CHECK_TIME).do(check_everyday_submission)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
