import requests
from constants import *
from typing import Any, Optional, Dict


def acquire_user_profile(username: str) -> Optional[Dict[str, Any]]:
    headers = API_HEADERS
    s = requests.Session()
    r = s.get(API_URL + username, headers=headers)
    csrf = r.cookies.get_dict()["csrftoken"]
    headers["cookie"] = "csrftoken=" + csrf
    headers["referer"] = API_URL + username
    data = API_QUERY % username
    r = s.post(
        API_URL + POSTFIX_GRAPHQL,
        cookies=s.cookies,
        data=data,
        headers=headers,
    )
    if r.status_code != 200:
        return None
    return r.json()


def get_user_solved_problem_count(
    user_profile: Optional[Dict[str, Any]]
) -> int:
    if user_profile is None:
        return 0
    accepted_submission_nums = user_profile["data"]["matchedUser"][
        "submitStats"
    ]["acSubmissionNum"]
    for submission_num in accepted_submission_nums:
        if submission_num["difficulty"] == "All":
            return submission_num["count"]
    return 0


if __name__ == "__main__":
    user_profile = acquire_user_profile("TommyTim0515")
    print(get_user_solved_problem_count(user_profile))
