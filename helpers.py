import logging
from pprint import pprint

from json import loads
from datetime import datetime
from typing import Dict, List

from db import existing_ids, add_new_posts
from config import (
    LOGGER,
    SEARCH_TERMS,
    REJECT_TERMS
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
            matches.append(search_term.lower() in post['title'].lower())

        # Check for terms that we will reject
        for reject_term in reject_terms:
            rejections.append(reject_term.lower() in post['title'].lower())

        accepted = any(matches) and not any(rejections)
        if accepted:
            filtered.append(post)

    LOGGER.debug(f'{sub}: Filtered {len(posts) - len(filtered)}/{len(posts)} posts, kept {len(filtered)}')
    return filtered


def format_response(posts: Dict) -> str:
    import ipdb; ipdb.set_trace()  # breakpoint 9173b049 //
    return ''
