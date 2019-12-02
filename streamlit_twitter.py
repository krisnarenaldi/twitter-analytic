import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import collections
import itertools
import matplotlib.pyplot as plt

import nltk
from nltk import bigrams
from nltk.corpus import stopwords

import networkx as nx

# pilih brand
option = st.sidebar.selectbox('Choose brand',['Adidas','Nike','Puma','Reebok','Vans'])
'You choose: ', option

#variabel file csv
fileNameOri = option.lower()+"_en_twitter.csv"   #"adidas_en_twitter.csv"
fileNameSentiment = option.lower()+"_en_twitter_sentiment.csv"


#INTRO
#
st.title("Twitter Analytic for "+option)
df = pd.read_csv(fileNameOri)

# SOURCE TWEET
st.header("Source Tweet")
sumber = df.groupby('source').size().reset_index(name='jumlah')
chart_data = pd.DataFrame(
                {
                'jumlah':sumber["jumlah"].tolist(),
                'source': sumber["source"].tolist()

             }
            )
chart_data = chart_data.rename(columns={'source':'index'}).set_index('index')
st.bar_chart(chart_data)


# WORD FREQUENCY
st.header("Word Frequency")
tweet_text = df[["text_complete"]]
tweet_text_list = tweet_text.values.tolist()
all_tweet_list = []
for tweet in tweet_text_list:
    all_tweet_list += tweet

words_in_tweet = [tweet.lower().split() for tweet in all_tweet_list]
all_words = list(itertools.chain(*words_in_tweet))
counts_words = collections.Counter(all_words)
df_counts_words = pd.DataFrame(counts_words.most_common(10),columns=['words','count'])
chart_data_wordfreq = pd.DataFrame(
    {
        'jumlah': df_counts_words["words"].tolist(),
        'word': df_counts_words["count"].tolist(),
    }
)
chart_data_wordfreq = chart_data_wordfreq.rename(columns={'word':'index'}).set_index('index')
st.bar_chart(chart_data_wordfreq)

# BIGRAM
st.header("CO-OCURRENCE BIGRAM AND NETWORK OF WORDS")
nltk.download("stopwords")
stop_words = set(stopwords.words('english'))
tweets_nsw = [[word for word in tweet_words if not word in stop_words] for tweet_words in words_in_tweet]

#remove colelction words
#collection_words = ['#adidas','adidas']
collection_words = ["#"+option.lower(),option.lower()]
tweets_nsw_nc = [[w for w in word if w not in collection_words] for word in tweets_nsw]
terms_bigram = [list(bigrams(tweet)) for tweet in tweets_nsw_nc]

mybigrams = list(itertools.chain(*terms_bigram))
mybigrams_count = collections.Counter(mybigrams)

bigram_df = pd.DataFrame(mybigrams_count.most_common(20),columns=['bigram','count'])
# print(bigram_df)

d = bigram_df.set_index('bigram').T.to_dict('records')
G = nx.Graph()

for k,v in d[0].items():
    G.add_edge(k[0],k[1],weight=(v*10))

#G.add_node("adidas",weight=100)
G.add_node(option.lower(),weight=100)

fig,ax = plt.subplots(figsize=(12,8))
pos = nx.spring_layout(G,k=1)

nx.draw_networkx(G,pos,font_size=16,width=3,edge_color='grey',node_color='purple',with_labels=False,ax=ax)

for key,value in pos.items():
    x,y = value[0]+.135,value[1]+.045
    ax.text(x,y,s=key,bbox=dict(facecolor='red',alpha=0.25),horizontalalignment='center',fontsize=13)

st.pyplot()

# SENTIMENT ANALYSIS
st.header("Sentiment Analytic")
# read file
dfs = pd.read_csv(fileNameSentiment)
sentimen = dfs.groupby('sentiment').size().reset_index(name='jumlah')
chart_data = pd.DataFrame(
                {
                'jumlah':sentimen["jumlah"].tolist(),
                'sentiment': sentimen["sentiment"].tolist()

             }
            )
chart_data = chart_data.rename(columns={'sentiment':'index'}).set_index('index')
st.bar_chart(chart_data)