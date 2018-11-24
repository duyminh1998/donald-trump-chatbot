import tweepy
import pandas as pd
import re

# API credentials
consumer_key = #
consumer_secret = #

access_token = #
access_token_secret = #

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# initialize a list to hold all the tweepy Tweets
alltweets = []
screen_name = 'realDonaldTrump'

# make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name = screen_name, count = 200, tweet_mode='extended')

# save most recent tweets
alltweets.extend(new_tweets)

# save the id of the oldest tweet less one
oldest = alltweets[-1].id

# keep grabbing tweets until there are no tweets left to grab
while len(new_tweets) >= 1:
       # all subsiquent requests use the max_id param to prevent duplicates
       new_tweets = api.user_timeline(screen_name = screen_name, count = 200, max_id = oldest, tweet_mode='extended')
       
       # save most recent tweets
       alltweets.extend(new_tweets)
       
       # update the id of the oldest tweet less one
       oldest = alltweets[-1].id

# initializes our DataFrame
df = pd.DataFrame(columns=['Tweets'])
i = 0

# filter
for tweet in alltweets:
	encoded = tweet.full_text.encode("utf-8", errors='ignore')

	# ignores URLs
	edited_tweet = re.sub(r'http\S+', '', str(encoded))

	# ignores emojis
	edited_tweet = re.sub(r'\\\w*', ' ', edited_tweet)

	# ignores retweets
	if edited_tweet != "b'":
	  edited_tweet = edited_tweet[2:].strip()
	  if edited_tweet[:2] != 'RT':
		  df.loc[i, 'Tweets'] = edited_tweet.strip()
		  i += 1

# appends new tweets to tweets we already have and saves to a csv
df = df.dropna()

master_df = pd.read_csv("data/master_tweets.csv")

pieces = [df, master_df]
new_master_df = pd.concat(pieces, sort=False)

new_master_df = new_master_df.drop_duplicates(subset = 'Tweets') # implement drop na
new_master_df.to_csv("data/master_tweets.csv", index = False)

