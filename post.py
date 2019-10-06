class Post():
    def __init__(self, post_json, title, url, subreddit):
        self.post_id = post_id
        self.title = title
        self.url = url
        self.subreddit = subreddit

    def __repr__(self):
        print(f'{self.subreddit}/{self.post_id}: {self.title} - [{self.url}]')
