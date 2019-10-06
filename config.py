from os import path
import logging
import sys


# --- Meta ---
ROOT_DIR = path.dirname(path.abspath(__file__))
APP_NAME = 'swap-watch'
VERSION = '0.1'


# --- Querying ---
USER_AGENT = f'python:{APP_NAME}:{VERSION}'
LIMIT = 5
SUBREDDITS = [
    'ULGearTrade',
    'hardwareswap'
]
JSON_URLS = [
    f'https://www.reddit.com/r/{subreddit}/new/.json?limit={LIMIT}' for subreddit in SUBREDDITS
]
SEARCH_TERMS = {
    'ULGearTrade': [
        'tarp',
        'quilt'
    ],
    'hardwareswap': [
        'mac'
    ]
}
REJECT_TERMS = {
    'ULGearTrade': [
        'wtb'
    ],
    'hardwareswap': [
        'cash'
    ]
}


# --- Database ---
IN_MEMORY = True
DB_NAME = 'test.db'


# --- Logging ---
LOGGER = logging.getLogger('app')
LOGGER.setLevel(logging.DEBUG)

# Create console handler, file handler, formatter, and set level to debug
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# Add handlers to logger
LOGGER.addHandler(ch)
LOGGER.addHandler(fh)
