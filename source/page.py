from flask import Flask, request, render_template
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

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
tweet_lst = []

def user_tweet(twitter_handle):
    tweets = api.user_timeline(screen_name=twitter_handle, count=50, tweet_mode="extended")
    clean = []
    for tweet in tweets:
        for word in tweet.full_text.split():
            if 'https:' in word or 'http:' in word or 'www' in word or '.com' in word:
                continue
            else:
                word_cloud_lst.append(word)
                clean.append(word)
        tweet_lst.append(" ".join(clean))
        clean = []

def generate_wordcloud(words, mask,handle):
    word_cloud = WordCloud(width = 512, height = 512, background_color='white', stopwords=STOPWORDS, mask=mask).generate(words)
    path = 'static/images/'+handle+'.png'
    word_cloud.to_file(path)
    word_cloud_lst = []

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    global word_cloud_lst
    word_cloud_lst = []
    handle = request.form['account']
    if handle == "" or handle == " ":
        return "invalid input"
    else:
        user_tweet(handle)
        words = " ".join(word_cloud_lst)
        mask = np.array(Image.open(requests.get('http://www.clker.com/cliparts/O/i/x/Y/q/P/yellow-house-hi.png', stream=True).raw))
        generate_wordcloud(words, mask,handle)
        filename = "images/{}.png".format(handle)
        return render_template('body.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
