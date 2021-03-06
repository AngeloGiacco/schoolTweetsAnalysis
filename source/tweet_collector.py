try:
    import tweepy
except ImportError:
    print("ENSURE YOU HAVE INSTALLED tweepy")
try:
    from credentials import *
except ImportError:
    print("ENSURE YOU HAVE CREATED credentials.py IN THE SAME FOLDER")
try:
    from wordcloud import WordCloud, STOPWORDS
except ImportError:
    print("ENSURE YOU HAVE INSTALLED wordcloud")
try:
    import requests
except ImportError:
    print("ENSURE YOU HAVE INSTALLED requests")
try:
    import numpy as np
except ImportError:
    print("ENSURE YOU HAVE INSTALLED numpy")

from PIL import Image
import urllib

meaningless_words = [
                    "il","la","az","ez","un","una",
                    "uno","gli","le","the","with","RT",
                    "amp","what","who","which","that",
                    "che","chi","con","I","del","di","della",
                    "ma","da","will"
                    ]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
word_cloud_lst = []

def user_tweet(twitter_handle):
    try:
        tweets = api.user_timeline(screen_name=twitter_handle, count=200, tweet_mode="extended")
        clean = []
        for tweet in tweets:
            for word in tweet.full_text.split():
                if 'https:' in word or 'http:' in word or 'www' in word or '.com' in word:
                    continue
                elif word[0] == "@":
                    continue
                else:
                    word_cloud_lst.append(word)
                    clean.append(word)
            clean = []
    except tweepy.TweepError:
        word_cloud_lst.append("invalid username")#a cool error message


def generate_wordcloud(words, mask):
    stopwords = set(STOPWORDS)
    for word in meaningless_words:
        stopwords.add(word)
    word_cloud = WordCloud(width = 512, height = 512, background_color='white', stopwords=stopwords, mask=mask).generate(words)
    path = 'static/images/'+handle+'.png'
    word_cloud.to_file(path)
    word_cloud_lst = []

if __name__ == '__main__':
    handle = "oundleschool"
    user_tweet(handle)
    words = " ".join(word_cloud_lst)
    mask = np.array(Image.open(requests.get('http://www.clker.com/cliparts/O/i/x/Y/q/P/yellow-house-hi.png', stream=True).raw))
    generate_wordcloud(words, mask)
