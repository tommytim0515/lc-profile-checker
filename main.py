import os
import glob
import account as ac
import configparser
import database
from constants import *
from typing import List


ACCOUNTS = []


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
    db = database.Database(DATABASE_NAME)
    for username in usernames:
        ACCOUNTS.append(ac.Account(username, 0, db))
    for account in ACCOUNTS:
        account.update_balance(0)


def main():
    init()
    for account in ACCOUNTS:
        print(f'{account.username}: {account.get_balance()}')


if __name__ == '__main__':
    main()
    # def decorator(func):
    #     def wrapper(*args, **kwargs):
    #         print('before')
    #         func(*args, **kwargs)
    #         print('after')
    #     return wrapper

    # @decorator
    # def test():
    #     print('test')

    # test()
