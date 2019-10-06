# TODO: Send email with response body
# TODO: Get html working in email body


from pprint import pprint

from requests import get
from typing import List, Dict

from logs import (
    LOGGER,
    LOGGER_RESULTS
)
from config import (
    USER_AGENT,
    SUBREDDITS,
    LIMIT
)
from helpers import (
    parse_json_response,
    filter_results,
    format_response
)

def grab_latest() -> List:
    """
    Grab the latest [LIMIT] posts from subreddits inside [SUBREDDITS]
    and filter them down to just a handful of relevant fields and remove
    posts that have already been parsed in the past.
    """
    # TODO: async requests, cuz fuggit
    posts = {}

    for sub in SUBREDDITS:
        pprint(sub)
        url = _get_subreddit_url(sub)
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

    message = format_response(posts)
    LOGGER_RESULTS.info(f'\n{message}')

def _get_subreddit_url(subreddit: str) -> str:
    return f'https://www.reddit.com/r/{subreddit}/new/.json?limit={LIMIT}'


if __name__ == "__main__":
    grab_latest()
