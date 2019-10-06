from datetime import datetime, timedelta
from requests import get
from typing import List, Dict, Callable

from send_email import send_email
from logs import (
    LOGGER,
    LOGGER_RESULTS
)
from config import (
    USER_AGENT,
    SUBREDDITS,
    SEARCH_TERMS,
    REJECT_TERMS,
    RECEIVER_EMAIL,
    EMAIL_NOTIFICATIONS,
    LIMIT,
    FREQUENCY,
)
from helpers import (
    parse_json_response,
    filter_results,
    format_response,
    format_subject
)

from apscheduler.schedulers.blocking import BlockingScheduler

SCHED = BlockingScheduler()


@SCHED.scheduled_job('interval', minutes=FREQUENCY * 60)
def grab_latest() -> List:
    """
    Grab the latest [LIMIT] posts from subreddits inside [SUBREDDITS]
    and filter them down to just a handful of relevant fields and remove
    posts that have already been parsed in the past.
    """
    # TODO: async requests, cuz fuggit
    posts = {}

    for sub in SUBREDDITS:
        url = _get_subreddit_url(sub)
        LOGGER.debug(f'Querying: {url}')
        response = get(
            url,
            headers={'User-Agent': USER_AGENT}
        )

        try:
            new_posts = parse_json_response(response.json())

        except Exception as e:
            LOGGER.exception(f'Request to {url} failed with code {response.status_code}: {response.reason}')

        # We got some posts we haven't seen before. Let's filter through them
        if new_posts:
            posts[sub] = filter_results(new_posts, sub)

    subject = format_subject(posts)
    message = format_response(posts)
    if not message:
        LOGGER_RESULTS.info('No new posts.')
        return

    LOGGER_RESULTS.info(f'\n{message}')

    if EMAIL_NOTIFICATIONS:
        send_email(subject, message)


def _get_subreddit_url(subreddit: str) -> str:
    return f'https://www.reddit.com/r/{subreddit}/new/.json?limit={LIMIT}'


if __name__ == "__main__":
    LOGGER.debug(
        f'App started, configured to run every {FREQUENCY * 60} minutes.\n'
        f'Running for subreddits: {SUBREDDITS} with following matching terms:\n'
        f'\tsearch: {SEARCH_TERMS}\n'
        f'\treject: {REJECT_TERMS}\n'
        f'Notifications being sent to {RECEIVER_EMAIL} and stored to \'results.log\'.'
    )
    grab_latest()
    SCHED.start()
