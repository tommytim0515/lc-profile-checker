from typing import Text
import requests
import json

headers = {
    'authority': 'leetcode.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'accept': '*/*',
    'accept-language': 'en',
    'content-type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'referer': '',
    'cookie': ''
}

query = '{"operationName": "getUserProfile","variables": {"username": "%s"},' \
        '"query": "query getUserProfile($username: String!) {\\n    ' \
        'matchedUser(username: $username) {\\n    username\\n    submissionCalendar\\n    ' \
        'submitStats: submitStatsGlobal {\\n    acSubmissionNum {\\n    difficulty\\n    ' \
        'count\\n    submissions\\n    __typename\\n    }\\n    __typename\\n    }\\n    __typename\\n}\\n}\\n"}'

url = 'https://leetcode.com/'


def get_user_info(username):
    s = requests.Session()
    # r = s.post(url, data=query, headers=headers)
    r = s.get(url+username, headers=headers)
    csrf = r.cookies.get_dict()['csrftoken']
    headers['cookie'] = 'csrftoken=' + csrf
    headers['referer'] = url+username
    data = query % username
    r = s.post(url+'graphql', cookies=s.cookies, data=data, headers=headers)
    print(r.text)


if __name__ == '__main__':
    get_user_info("TommyTim0515")
