# database
DATABASE_DIR = "db"
DATABASE_NAME = "test_storage"
LAST_UPDATE_KEY = "last_update"
MUTEX_KEY = "mutex"
UNDISTRIBUTED_KEY = "undistributed"
DATETIME_FORMAT = "%Y-%m-%d"
BALANCE_PREFIX = "balance_"
ACCEPTED_PREFIX = "accepted_"

# web scraping
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
URL_PREFIX = "https://leetcode.com/"
ACCPET_KEYWORD = "Accepted"
ACCEPT_TOKENS = ("minute", "minutes", "hour", "hours")
PAGE_LOAD_TIME = 5  # seconds
EXTENDED_PAGE_LOAD_TIME = 10  # seconds
RETRY_NUM = 5

# leetcode API
API_URL = "https://leetcode.com/"
API_HEADERS = {
    "authority": "leetcode.com",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", '
    '"Google Chrome";v="96"',
    "accept": "*/*",
    "accept-language": "en",
    "content-type": "application/json",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "referer": "",
    "cookie": "",
}
API_QUERY = (
    '{"operationName": "getUserProfile","variables": {"username": "%s"},'
    '"query": "query getUserProfile($username: String!) {\\n    '
    "matchedUser(username: $username) {\\n    "
    "username\\n    submissionCalendar\\n    "
    "submitStats: submitStatsGlobal {\\n    "
    "acSubmissionNum {\\n    difficulty\\n    "
    "count\\n    submissions\\n    __typename\\n    }\\n    __typename\\n    "
    '}\\n    __typename\\n}\\n}\\n"}'
)
POSTFIX_GRAPHQL = "graphql"

# main
CONFIG_FILE_DIR = "config.ini"
DEPOSIT = 5
CHECK_TIME = "00:30"
