import sys
from os import path
from json import load

# --- Meta ---
ROOT_DIR = path.dirname(path.abspath(__file__))
CONFIG_FILE_DIR = f'{ROOT_DIR}/config.json'
APP_NAME = 'swap-watch'
VERSION = '0.1'


# --- Read from config.json ---
with open(CONFIG_FILE_DIR) as config_file:
    CONFIG = load(config_file)


# --- Frequency ---
# How many times to run the query in hours.
FREQUENCY = CONFIG['frequency']


# --- Emails ---
SENDER_EMAIL = CONFIG['email']['sender_email']
PASSWORD = CONFIG['email']['sender_email_password']
RECEIVER_EMAIL = CONFIG['email']['receiver_email']


# --- Querying ---
USER_AGENT = f'python:{APP_NAME}:{VERSION}'
LIMIT = CONFIG['queries']['limit']
SUBREDDITS = CONFIG['queries']['subreddits']
SEARCH_TERMS = CONFIG['queries']['search_terms']
REJECT_TERMS = CONFIG['queries']['reject_terms']


# --- Database ---
IN_MEMORY = CONFIG['database']['in_memory']
DB_NAME = CONFIG['database']['db_name']
