import os
import time
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
        'usernames': config['USER']['usernames'],
    }


def get_usernames(config: dict) -> List:
    return config['usernames'].split(',')


def init():
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    previous_db_files = glob.glob(os.path.join(DATABASE_DIR, '*'))
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
    for account in ACCOUNTS:
        print(f'{account.username}: {account.get_balance()}')
    print(f'Undistributed: {DATABASE.get_undistributed_balance()}')


def check_everyday_submission():
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    DATABASE.update_undistributed_balance(
        current_undistributed_balance + DEPOSIT * len(ACCOUNTS))
    finished_accounts = []
    for account in ACCOUNTS:
        if account.check_today_submission():
            finished_accounts.append(account)
    if len(finished_accounts) <= 0:
        return
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    reward_per_account = current_undistributed_balance // len(
        finished_accounts)
    for account in finished_accounts:
        account.update_balance(account.get_balance() + reward_per_account)
    DATABASE.update_undistributed_balance(
        current_undistributed_balance - reward_per_account * len(finished_accounts))


def check_everyday_accepted():
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    DATABASE.update_undistributed_balance(
        current_undistributed_balance + DEPOSIT * len(ACCOUNTS))
    finished_accounts = []
    for account in ACCOUNTS:
        accepted_num = account.check_today_accepted()
        prev_ac_num, _ = account.get_accepted_num_and_time()
        if accepted_num > prev_ac_num:
            finished_accounts.append(account)
        account.update_accepted_num_and_time(accepted_num)
    if len(finished_accounts) <= 0:
        return
    current_undistributed_balance = DATABASE.get_undistributed_balance()
    reward_per_account = current_undistributed_balance // len(
        finished_accounts)
    for account in finished_accounts:
        account.update_balance(account.get_balance() + reward_per_account)
    DATABASE.update_undistributed_balance(
        current_undistributed_balance - reward_per_account * len(finished_accounts))


def print_info():
    for account in ACCOUNTS:
        accepted_num, _ = account.get_accepted_num_and_time()
        print(f'{account.username}:\n Balance: {account.get_balance()}, Accepted: {accepted_num}')
    print(f'Undistributed: {DATABASE.get_undistributed_balance()}')
    print(datetime.now())


def main():
    init()
    if DATABASE is None:
        print('Database not initialized.')
    print(datetime.now())
    # check_everyday_submission()
    # check_everyday_accepted()
    # print_info()
    schedule.every().day.at(CHECK_TIME).do(check_everyday_accepted)
    # schedule.every(5).minutes.do(check_everyday_submission)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
