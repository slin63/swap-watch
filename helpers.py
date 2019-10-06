import logging
import math

from json import loads
from datetime import datetime, timedelta
from typing import Dict, List

from db import existing_ids, add_new_posts
from config import (
    LOGGER,
    SEARCH_TERMS,
    REJECT_TERMS,
    APP_NAME
)

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
        matches = []
        rejections = []

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


def format_response(posts: Dict) -> str:
    header = f'{APP_NAME} results for [{datetime.now()}]:'
    body = ''
    for sub in posts:
        new_posts = posts[sub]
        for post in new_posts:
            post_str = _format_post(post)

    return ''


def _format_post(post: Dict) -> str:
    link_post = __hyperlink(post['url'], post['title'])
    link_message = __hyperlink(f"https://www.reddit.com/message/compose/?to={post['username']}", f"Message {post['username']} now!")
    matched_because = f"Matching terms: <b>{', '.join(post['matches'])}</b>"
    time_since_post = __human_readable_timedelta(datetime.now() - post['created_utc'])

    body = f"""
<h4>{link_post}</h4>
<h5>Posted {time_since_post}.</h5>
<h5>{link_message}</h5>
{matched_because}
"""

    return body


def __hyperlink(url: str, text: str) -> str:
    return f'<a href=\"{url}\">{text}</a>'


def __human_readable_timedelta(dt: timedelta) -> str:
    """
    Return a human readable time delta, assuming posts will never be more than 10 days old.
    """
    days = math.floor(dt.seconds / 86400)
    hours = math.floor((dt.seconds - (math.floor(days) * 86400)) / 3600)
    minutes = math.floor((dt.seconds - (math.floor(hours) * 3600)) / 60)

    # Timedelta less than one hour
    if not hours and not days and minutes:
        return f'{minutes} minutes ago'

    # Timedelta less than one day
    elif not days and hours:
        return f'{hours} hours and {minutes} minutes ago'

    # Timedelta one day or greater
    elif days:
        if days == 1:
            return 'yesterday'
        else:
            return f'{days} days ago'

    else:
        return 'just now'
