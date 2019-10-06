from sqlite3 import connect
from config import DB_NAME, ROOT_DIR, IN_MEMORY
from typing import List, Tuple, Dict

if IN_MEMORY:
    CONNECTION = connect(':memory:')
else:
    CONNECTION = connect(f'{ROOT_DIR}/{DB_NAME}')
CURSOR = CONNECTION.cursor()

# Initialize tables and clear posts older than ten days
CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS posts (
    id text PRIMARY KEY,
    title text,
    url text,
    subreddit text,
    create_date text);
''')

CURSOR.execute('''
    DELETE FROM posts WHERE create_date <= date('now', '-10 day')
''')

CONNECTION.commit()


def add_new_posts(new_posts: List[Dict]) -> int:
    to_insert = []
    for post in new_posts:
        to_insert.append(tuple(post.values()))

    insert_statement = CURSOR.executemany(f'''
        INSERT INTO posts (id, title, url, subreddit, create_date) VALUES (?, ?, ?, ?, ?)
    ''', to_insert)

    CONNECTION.commit()

    return insert_statement.rowcount


def existing_ids() -> List[str]:
    """
    Return a list of existing post ids so that we don't send duplicate
    notifications for posts the user has already seen.
    """
    existing_ids = CURSOR.execute(f'''
        SELECT id FROM posts;
    ''').fetchall()

    # Unpack the tuple results
    existing_ids = [result[0] for result in existing_ids]

    return existing_ids
