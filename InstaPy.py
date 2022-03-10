from instapy import InstaPy 
from instapy import smart_run
import random as r
import schedule 
import time # 

# Insert your Instagram username, as well as password below
username = ""
password = ""

# Function to handle all the actions the bot will take
def bot():
    session = InstaPy(username=username, password=password,
                      headless_browser=True, 
                      disable_image_load=True,
                      multi_logs=True)
    session.login() # Creating and logging into session

    # Searched for a long time trying to figure out what smart_run does.
    # If you know what smart_run does please let me know.
    with smart_run(session):
        session.like_by_tags(["programming"], sort='recent', amount=50) 
        session.set_ignore_if_contains(['sex', 'second', 'account'])
        session.set_do_follow(True, percentage=r.randint(50, 80)) # Setting percent chance that the bot will follow the user.
        session.set_skip_users(skip_private=True,
                       private_percentage=100,
                       skip_business=True,
                       business_percentage=100)
        session.set_relationship_bounds(enabled=True,
                                potency_ratio=1,
                                delimit_by_numbers=True,
                                max_followers=2000,
                                max_following=1000,
                                min_followers=50,
                                min_following=20,
                                min_posts=5,
                                max_posts=2000)
        session.set_action_delays(enabled=True,
                           like=3,
                           follow=4,
                           unfollow=28,
                           randomize=True,
                           random_range_from=70,
                           random_range_to=140)
        
# Setting the time at which the bot should run each day (as long as the bot is running)
schedule.every().day.at(f"09:46").do(bot)
schedule.every().day.at(f"18:12").do(bot)

# Below loop will check every 15 seconds if there are any pending sessions that the bot needs to do.
while True:
    schedule.run_pending()
    time.sleep(15)
