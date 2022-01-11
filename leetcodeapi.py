import requests
from datetime import datetime, timedelta
from constants import *
from typing import Any, Optional, Dict, Tuple, List


def make_session(username: str) -> Tuple[requests.Session, Dict[str, str]]:
    headers = API_HEADERS
    s = requests.Session()
    r = s.get(API_URL + username, headers=headers)
    csrf = r.cookies.get_dict()["csrftoken"]
    headers["cookie"] = "csrftoken=" + csrf
    headers["referer"] = API_URL + username
    return s, headers


def acquire_user_profile(
    session: requests.Session, headers: Dict[str, Any], username: str
) -> Optional[Dict[str, Any]]:
    data = API_USER_PROFILE_QUERY % username
    r = session.post(
        API_URL + POSTFIX_GRAPHQL,
        cookies=session.cookies,
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


def acquire_recent_submission_list(
    session: requests.Session, headers: Dict[str, Any], username: str
) -> Optional[Dict[str, Any]]:
    data = API_RECENT_SUBMISSION_QUERY % username
    r = session.post(
        API_URL + POSTFIX_GRAPHQL,
        cookies=session.cookies,
        data=data,
        headers=headers,
    )
    if r.status_code != 200:
        return []
    return r.json()["data"]["recentSubmissionList"]


def get_yesterday_accepted_submissions(
    submission_list: Dict[str, Any]
) -> List[Tuple[str, str]]:
    set_accepted_title_slug_and_lang = set()
    yesterday_accepted_submission = []
    for submission in submission_list:
        if submission["statusDisplay"] != "Accepted":
            continue
        if datetime.fromtimestamp(
            int(submission["timestamp"])
        ).date() < datetime.now().date() - timedelta(days=1):
            continue
        title_slug_and_lang = submission["titleSlug"] + submission["lang"]
        if title_slug_and_lang in set_accepted_title_slug_and_lang:
            continue
        set_accepted_title_slug_and_lang.add(title_slug_and_lang)
        yesterday_accepted_submission.append(
            (submission["title"], submission["lang"])
        )
    return yesterday_accepted_submission


if __name__ == "__main__":
    session, headers = make_session("TommyTim0515")
    user_profile = acquire_user_profile(session, headers, "TommyTim0515")
    print(get_user_solved_problem_count(user_profile))
    submission_list = acquire_recent_submission_list(session, headers, "TommyTim0515")
    print(get_yesterday_accepted_submissions(submission_list))
