from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from flask import Flask, jsonify
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re

app = Flask(__name__)

# Init
newsapi = NewsApiClient(api_key='833713696660479590fc3778d8796e4c')

# top headlines provided by google news API
top_headlines = newsapi.get_top_headlines(page_size=30, language='en')
# top headlines on CNN
top_headlines_cnn = newsapi.get_top_headlines(page_size=30, sources='cnn',
                                              language='en')
# top headlines on Fox
top_headlines_fox = newsapi.get_top_headlines(page_size=30, sources='fox-news',
                                              language='en')

# all news sources which match with language english and location us
news_sources = newsapi.get_sources(language='en',country='us')
# print(top_headlines)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/news")
def top_news():
    filled_entries = []
    for article in top_headlines['articles']:
        if article['title'] and article['description'] and article['url'] and article['urlToImage']:
            if(len(filled_entries) < 5):
                filled_entries.append(article)
    return jsonify({'news':filled_entries})

@app.route("/cnn")
def cnn_news():
    filled_entries = []
    for article in top_headlines_cnn['articles']:
        if article['title'] and article['description'] and article['url'] and article['urlToImage']:
            if (len(filled_entries) < 4):
                filled_entries.append(article)
    return jsonify({'cnn': filled_entries})

@app.route("/fox")
def fox_news():
    filled_entries = []
    for article in top_headlines_fox['articles']:
        if article['title'] and article['description'] and article['url'] and article['urlToImage']:
            if (len(filled_entries) < 4):
                filled_entries.append(article)
    return jsonify({'fox': filled_entries})

@app.route("/sources")
def sources():
    filled_entries = []
    for source in news_sources['sources']:
        if source['name'] and source['id'] and source['category']:
            filled_entries.append(source)
    return jsonify({'sources': filled_entries})

@app.route("/sources/<category>")
def categorized_sources(category):
    categorized_news_services = newsapi.get_sources(category=category, language='en', country='us')
    filled_entries = []
    for source in categorized_news_services['sources']:
        if source['name'] and source['id'] and source['category']:
            filled_entries.append(source)
    return jsonify({'sources': filled_entries})

@app.route("/results/<query>")
def news_results(query):
    # expect input of format q-source-from-to
    params = re.split("!", query)
    print(params)
    if params[1] == 'all':
        params[1] = ''
    all_news_results = None
    try:
        all_news_results = newsapi.get_everything(q=params[0], sources=params[1], from_param=params[2], to=params[3], sort_by='relevancy', language='en')
    except NewsAPIException as e:
        return jsonify({'status': 'error', 'message': e.get_message()})
    filled_entries = []
    for result in all_news_results['articles']:
        if result['author'] and result['title'] and result['description'] and result['url'] and result['urlToImage'] and result['publishedAt'] and result['source'] and result['source']['name']:
            if(len(filled_entries) < 10):
                filled_entries.append(result)
    return jsonify({'status': 'ok', 'articles': filled_entries})

@app.route("/words")
def top_words():
    words = []
    final_words = []
    cnt = Counter()
    stop_words = set(stopwords.words('english'))
    descs = []
    for article in top_headlines['articles']:
        if(article['description']):
            descs.append(article['description'])

    for desc in descs:
        tokens = word_tokenize(desc)
        # print(tokens)
        words.extend(tokens)

    for word in words:
        if word not in stop_words and len(word) > 3:
            final_words.append(word)

    frequent_words = sorted(list(dict(Counter(final_words)).items()), key=lambda k: (-k[1],k[0]))[:30]
    most_frequent = [{'w': k, 'c': v} for k,v in frequent_words]
    return jsonify({'words': most_frequent})

if __name__ == "__main__":
    app.run(debug=False)