from instapy import InstaPy 
from instapy import smart_run
import random as r
import time 

username = ""
password = ""

session = InstaPy(username=username, password=password,
                  headless_browser=True, 
                  disable_image_load=True,
                  multi_logs=True)

with smart_run(session):
    session.like_by_tags(["programming"], amount=1) 
    session.set_ignore_if_contains(['sex', 'second', 'account', '부계정', 'bot', '팔로우'])
    session.set_do_follow(enabled=True, percentage=r.randint(50, 80), times=1)
    
    session.set_quota_supervisor(enabled=True,
                            sleep_after=["likes", "follows", "unfollows"],
                            sleepyhead=True,
                            stochastic_flow=True,
                            notify_me=True,
                            peak_likes_hourly=30,
                            peak_likes_daily=300,
                            peak_follows_hourly=5,
                            peak_follows_daily=30,
                            peak_unfollows_hourly=10,
                            peak_unfollows_daily=100)
    
    session.set_skip_users(skip_private=True,
                           private_percentage=100,
                           skip_business=True,
                           business_percentage=100)
    
    session.set_relationship_bounds(enabled=True,
                                potency_ratio=1,
                                delimit_by_numbers=True,
                                max_followers=1000,
                                max_following=1000,
                                min_followers=60,
                                min_following=50,
                                min_posts=5,
                                max_posts=100)
    
    session.set_action_delays(enabled=True,
                           like=6,
                           follow=10,
                           unfollow=30,
                           randomize=True,
                           random_range_from=70,
                           random_range_to=140)
session.end()
print("Session End")
        
