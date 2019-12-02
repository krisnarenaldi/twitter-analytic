import pandas as pd
import numpy as np
import collections
import itertools
import matplotlib.pyplot as plt

import nltk
from nltk import bigrams
from nltk.corpus import stopwords

import networkx as nx

#variabel
## filename
fileNameOri = "adidas_en_twitter.csv"
fileNameOri10 = "adidas_en_twitter_10.csv"
fileNameSentiment = "adidas_en_twitter_sentiment.csv"
all_tweet_list = []

# read file
df = pd.read_csv(fileNameOri10)

# SOURCE TWEET
print("SOURCE TWEET")
sumber = df.groupby('source').size().reset_index(name='jumlah')
print(sumber)
print("+="*50)

# WORD FREQUENCY
print("WORD FREQUENCY")
tweet_text = df[["text_complete"]]
tweet_text_list = tweet_text.values.tolist()

for tweet in tweet_text_list:
    all_tweet_list += tweet

words_in_tweet = [tweet.lower().split() for tweet in all_tweet_list]
# print(words_in_tweet)

all_words = list(itertools.chain(*words_in_tweet))
counts_words = collections.Counter(all_words)
df_counts_words = pd.DataFrame(counts_words.most_common(10),columns=['words','count'])
print(df_counts_words)
print("+="*50)

# BIGRAM
print("BIGRAM")
nltk.download("stopwords")
stop_words = set(stopwords.words('english'))
# all_words = [word for word in words_in_tweet]
# print(all_words)
tweets_nsw = [[word for word in tweet_words if not word in stop_words] for tweet_words in words_in_tweet]
# print(tweets_nsw)

#remove colelction words
collection_words = ['#adidas','adidas']
tweets_nsw_nc = [[w for w in word if w not in collection_words] for word in tweets_nsw]
# print(tweets_nsw_nc)

terms_bigram = [list(bigrams(tweet)) for tweet in tweets_nsw_nc]
# print(terms_bigram[0])
mybigrams = list(itertools.chain(*terms_bigram))
mybigrams_count = collections.Counter(mybigrams)

bigram_df = pd.DataFrame(mybigrams_count.most_common(20),columns=['bigram','count'])
print(bigram_df)

# d = bigram_df.set_index('bigram').T.to_dict('records')
# G = nx.Graph()
#
# for k,v in d[0].items():
#     G.add_edge(k[0],k[1],weight=(v*10))
#
# G.add_node("off",weight=100)
#
# fig,ax = plt.subplots(figsize=(10,8))
# pos = nx.spring_layout(G,k=1)
#
# nx.draw_networkx(G,pos,font_size=16,width=3,edge_color='grey',node_color='purple',with_labels=False,ax=ax)
#
# for key,value in pos.items():
#     x,y = value[0]+.135,value[1]+.045
#     ax.text(x,y,s=key,bbox=dict(facecolor='red',alpha=0.25),horizontalalignment='center',fontsize=13)

# plt.show()
print("+="*50)

# SENTIMENT ANALYSIS
print("SENTIMENT ANALYSIS")

# read file
dfs = pd.read_csv(fileNameSentiment)
sentimen = dfs.groupby('sentiment').size().reset_index(name='jumlah')
print(sentimen)
print("+="*50)

