![Trump Bot](https://img.thedailybeast.com/image/upload/c_crop,d_placeholder_euli9k,h_1439,w_2560,x_0,y_0/dpr_2.0/c_limit,w_740/fl_lossy,q_auto/v1492108180/galleries/2016/11/07/2016-s-best-election-memes/160525-pepe-trump-tease_h8fkou)
# donald-trump-chatbot
This is a chatbot that learns from Donald Trump's tweets to replicate the experience of talking to your very own Chief Executive. 

### Goals
- ~Scrape Tweets~
- ~Script Trump Bot~
- Use Flask to create website for bot, allowing us to retrieve more user - bot response
- Implement rating system for each user - bot interaction
- Improve ML model

### 11/24/18
We are still in the processing of pairing user response and possible bot responses. Tensorflow and deep learning might be a better model for our chatbot (longevity)

What we did this meeting:
- Paired user response with possible bot response (tweets)
- Created a skeleton/template of what the bot could look like **trump_bot.py**

What we plan to do next meeting:
- Finalize user - bot response pair
- Look into Tensorflow as a deep learning model for the chatbot

### 10/30/18
Generated a list of possible user response to pair with the bot response (Tweets). We also explored Spacy for NLP. We will be using 
`nlp.similarity()` to determine the similarity between an actual user's response to the possible user response in our database. We then output the paired bot response. This process is actually quite fast but is dependent on the quality and quantity of our user - bot response pair database. 

What we did this meeting:
- Read Spacy documentation
- Scraped Tinder dating sites to generate possible user response

What we plan to do next meeting:
- Pair more user - bot response
- Read implementations of chatbots

### 10/23/18
We explore scraping Donald Trump's tweets. Athough there are already available datasets, they are not recent. We use the Tweepy API to scrape the tweets.

What we did this meeting:
- Created **twitter_scrape.py** to scrape the tweets
- Stored the tweets in the **master_tweets.csv** file

What we plan to do next meeting:
- Scrape more tweets / set up Stream for continuous Tweet scraping
- Explore ML models
