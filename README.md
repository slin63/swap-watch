# swap-watch
![demo](https://i.imgur.com/SoQXR0T.png)
A tool that watches for spicy deals from your favorite `r/<thing>swap` Subreddits and notifies you with the latest updates.

## Setup
1. Clone this repo to your local machine: `$ git clone https://github.com/slin63/swap-watch && cd swap-watch`
2. Install dependencies with `$ pipenv install`
3. Create a new `config.json`: `$ cp sample_config.json config.json`
  - Note that you can skip adding your email credentials for now and just stick to receiving notifications through the console.
4. Fill out the config as shown below in the **Config Walkthrough** section
5. Run the script using `$ pipenv run python main.py`
6. Receive notifications through both the email you specified and the console view.

## Config Walkthrough
```
"frequency": 0.25,
    - Time in hours between each query.
    For example, "frequency": 0.25 means to check the subreddits every 15 minutes.
```
```
"email": {
    "sender_email": "sample_email@gmail.com",
        - The Gmail account that will be sending out email notifications.
        It's recommended you create an account specific for this purpose as
        the account will need to have "Less secure app access" enabled as shown here:
        https://support.google.com/accounts/answer/6010255
    "sender_email_password": "p@ssw0rDz",
        - The password for your sender email.
    "receiver_email": "your_email@gmail.com",
        - The address you want the notifications sent to.
    "email_notifications": false
        - Whether or not to receive email notifications. You can leave
        this false if you don't want to provide any email credentials.
```
```
"queries": {
    "limit": 25,
        - How many new posts to scrape at a time.
    "subreddits": [
        "ULGearTrade",
        "hardwareswap"
    ],
        - A list of subreddits you want to scrape.
    "search_terms": {
        "ULGearTrade": [
            "quilt",
            "pack"
        ],
        "hardwareswap": [
            "mac"
        ]
    },
        - A key:value list of terms to search for in the titles of the posts from
        each respective subreddit.
        Can be left empty to just grab all posts.
    "reject_terms": {
        "ULGearTrade": [
            "wtb",
            "damaged"
        ],
        "hardwareswap": [
            "for parts"
        ]
    }
        - A key:value list of terms to use to ignore posts from each respective subreddit.
},
```
```
"database": {
    "in_memory": true,
        - Whether or not to use an in memory database. Strictly for testing purposes.
    "db_name": "swap-watch.db"
        - The name to use for the database.
}
```
