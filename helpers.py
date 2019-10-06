import logging
import math

from json import loads
from datetime import datetime, timedelta
from typing import Dict, List

from db import existing_ids, add_new_posts
from config import (
    SEARCH_TERMS,
    REJECT_TERMS,
    APP_NAME
)
from logs import LOGGER


def parse_json_response(json_response: Dict) -> List[Dict]:
    """
    Condense a JSON response down to just essential information about
    posts and remove any posts that have already been parsed in past requests
    """
    posts = json_response['data']['children']
    new_posts = []

    for post in posts:
        post = post['data']
        post_id = post['id']
        subreddit = post['subreddit']

        # We haven't seen this post before, parse it and queue it to add to database
        if post_id not in existing_ids():
            new_posts.append({
                'id': post_id,
                'title': post['title'],
                'url': post['url'],
                'subreddit': post['subreddit'],
                'username': post['author'],
                'created_utc': datetime.fromtimestamp(post['created_utc']),
            })

    if new_posts:
        inserted = add_new_posts(new_posts)
        LOGGER.debug(f"Added {inserted} new posts to {subreddit}")

    return new_posts


def filter_results(posts: List[Dict], sub: str) -> List[Dict]:
    search_terms = SEARCH_TERMS[sub]
    reject_terms = REJECT_TERMS[sub]

    filtered = []

    for post in posts:
        # Handle if user doesn't specify search or reject keywords
        matches = [] if search_terms else [True]
        rejections = [] if reject_terms else [False]

        # Check for terms that match what we're looking for
        for search_term in search_terms:
            match = search_term.lower() in post['title'].lower()
            matches.append(match)
            if match:
                if post.get('matches'):
                    post['matches'].append(search_term)
                else:
                    post['matches'] = [search_term]

        # Check for terms that we will reject
        for reject_term in reject_terms:
            rejections.append(reject_term.lower() in post['title'].lower())

        accepted = any(matches) and not any(rejections)
        if accepted:
            filtered.append(post)

    LOGGER.debug(f'{sub}: Filtered {len(posts) - len(filtered)}/{len(posts)} posts, kept {len(filtered)}')
    return filtered


def format_subject(posts: Dict) -> str:
    subj = '[Swap-Watch]: '
    subs = posts.keys()
    new_post_count = 0
    for sub in posts:
        new_post_count += len(posts[sub])

    if new_post_count:
        post_str = 'posts' if new_post_count > 1 else 'post'
        subj += f"{new_post_count} new posts for {', '.join(subs)}"

    return subj


def format_response(posts: Dict) -> str:
    header = f'{APP_NAME} results for [{datetime.now()}]:'
    body = ''

    for sub in posts:
        new_posts = posts[sub]
        if new_posts:
            body += f'r/{sub} results:'

            for post in new_posts:
                body += _format_post(post)

            body += '\n'

    return body.strip()


def _format_post(post: Dict) -> str:
    link_message = f"Message poster: https://www.reddit.com/message/compose/?to={post['username']}"
    if not post.get('matches'):
        matched_because = f"No matching keys specified for this subreddit."
    else:
        matched_because = f"Matching terms: {', '.join(post.get('matches', []))}."
    time_since_post = __human_readable_timedelta(datetime.now() - post['created_utc'])

    body = f"""
->  {post['title']}
        {post['url']}
        Posted {time_since_post}.
        {link_message}
        {matched_because}
"""

    return body



def __human_readable_timedelta(dt: timedelta) -> str:
    """
    Return a human readable time delta, assuming posts will never be more than 10 days old.
    """
    days = math.floor(dt.seconds / 86400)
    hours = math.floor((dt.seconds - (math.floor(days) * 86400)) / 3600)
    minutes = math.floor((dt.seconds - (math.floor(hours) * 3600)) / 60)

    # Properly render plural or non-plural time units
    minute_str = 'minutes' if minutes > 1 else 'minute'
    hour_str = 'hours' if hours > 1 else 'hour'

    # Timedelta less than one hour
    if not hours and not days and minutes:
        return f'{minutes} {minute_str} ago'

    # Timedelta less than one day
    elif not days and hours:
        return f'{hours} {hour_str} and {minutes} {minute_str} ago'

    # Timedelta one day or greater
    elif days:
        if days == 1:
            return 'yesterday'
        else:
            return f'{days} days ago'

    else:
        return 'just now'
