import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# vader
analyser = SentimentIntensityAnalyzer()
sentiment_score = 0
sentiment_string = {"0":"Neutral","1":"Positif","-1":"Negatif"}
sentiment_value = "Neutral"

#variabel
linenum = 0
mylist = [('username','screenname', 'created_at','tweet_text','sentiment')]

# sentiment_result = analyser.polarity_scores("Star Collaboration is coming")
# print(sentiment_result)

# fungsi
def sentiment_analyzer_score(mytext):
    score = analyser.polarity_scores(mytext)

    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif (lb>-0.05) and (lb < 0.05):
        return 0
    else:
        return -1

with open("adidas_en_twitter.csv","r") as csvfile:
    readCsv = csv.reader(csvfile,delimiter=",")
    for row in readCsv:
        if linenum > 0:
            sentiment_score = sentiment_analyzer_score(row[6])
            sentiment_value = sentiment_string[str(sentiment_score)]
            _tuple = (row[1],row[2],row[3],row[6],sentiment_value)
            mylist.append(_tuple)
        linenum += 1

linenum = 0
with open("adidas_en_twitter_sentiment.csv","w") as writefile:
    csvWrite = csv.writer(writefile)
    for row in mylist:
        csvWrite.writerow(row)

print("Done!")
