import tweepy
import time
from keys import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

# * PATH TO THE FILE WHERE LAST PROCESSED MENTION'S ID IS STORED
FILE_NAME = r'D:\Projects\Twitter_Bot\OAuth API Bot\last_id.txt'


# * USED FOR STORING THE ID OF LAST PROCESSED MENTION..
def retrieve_last_id(file_name):
    f_read = open(file_name, 'r')
    last_id = int(f_read.read().strip())
    f_read.close()
    return last_id


# * USED FOR STORING THE ID OF LAST PROCESSED MENTION..
def store_last_id(last_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_id))
    f_write.close()
    return


# * USED FOR REPLYING TO THE TWEETS THAT MENTIONED ME..
def reply_tweets():
    last_id = retrieve_last_id(FILE_NAME)
    mentions = api.mentions_timeline(last_id, tweet_mode='extended')
    for mention in reversed(mentions):
        print('\nMention By: @' + mention.user.screen_name)
        print('Mention ID: ' + str(mention.id))
        print(mention.full_text)
        api.update_status('@' + mention.user.screen_name + ' Thanks for mentioning me',
                          in_reply_to_status_id=mention.id, auto_populate_reply_metadata=True)
        print('Thanking user')
        time.sleep(5)
        mention.favorite()
        print('Mention Liked')
        time.sleep(5)
        mention.user.follow()
        print('User Followed')
        time.sleep(5)
        last_id = mention.id
        store_last_id(last_id, FILE_NAME)
        time.sleep(5)


# * USED FOR SEARCHING AND PROCESSING THE STRING '#100DAYSODCODE'..
def promote_coding():
    print('\nPromoting coders everywhere!!')
    for tweet in tweepy.Cursor(api.search, '#100daysofcode').items(100):
        if tweet.retweet_count == 0:
            print('\nTweet by: @' + tweet.user.screen_name)
            print('ID: @' + str(tweet.user.id))
            print(tweet.text)
            if tweet.favorited == False:
                tweet.favorite()
                print('Liked!!')
                tweet.favorited = True
                time.sleep(5)
                tweet.retweet()
                print('Retweeted!!')
                tweet.retweeted = True
                time.sleep(5)
            else:
                continue
        else:
            continue
    return


# * USED FOR FOLLOWING ALL MY FOLLOWERS..
def follow_followers():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        time.sleep(5)
    print('\nFollowed everyone who is following me!!')


c = 0
while True:
    c += 1
    c %= 5
    print(c)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    if c == 0:
        follow_followers()
        time.sleep(60)
    reply_tweets()
    time.sleep(60)
    if c == 0:
        promote_coding()
        time.sleep(60 * 10)
