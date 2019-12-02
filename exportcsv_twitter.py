import basic
from pandas import DataFrame
import sys
import numpy as np
import re


#fungsi
def remove_pattern(input_txt, mypattern):
    goregex = re.findall(mypattern, input_txt)
    for res in goregex:
        input_txt = re.sub(res," ",input_txt)
    return input_txt

def remove_nonchar(input_txt):
    input_txt = "".join(e for e in input_txt if e.isalnum())
    return input_txt

def remove_nonchar2(text_list):
    index = 0
    for t in text_list:
        if t.isalnum() or t.startswith("#") == False:
            text_list.pop(index)
    index += 1
    return text_list

def clean_text(mytext):
    #remove RT
    mytext = np.vectorize(remove_pattern)(mytext,"RT @[\w]*:")
    #remove mention
    mytext = np.vectorize(remove_pattern)(mytext,"@[\w]*")
    #remove url
    mytext = np.vectorize(remove_pattern)(mytext,"https?://[A-Za-z0-9./]*")
    #remove non-ascii
    mytext = np.vectorize(remove_pattern)(mytext,"[^\x00-\x7f]")
    #remove white space
    mytext = np.vectorize(remove_pattern)(mytext,"\s+")
    #remove new line
    mytext = np.core.defchararray.replace(mytext,"\n+","")

    return mytext

#variabel
sql = "SELECT tw.id,tu.name,tu.screen_name,tw.tweet_created_at,tw.id_tweet,tw.id_tweet_origin,tw.text_complete," \
      "tw.hashtags,tw.symbols,tw.has_media,tw.has_users_mention," \
      "tw.has_urls_mention,tw.source,tw.in_reply_to_status_id,tw.in_reply_to_user_id," \
      "tw.in_reply_to_screen_name,tw.contributors,tw.is_quote_status,tw.retweet_count," \
      "tw.favorite_count,tw.favorited,tw.retweeted,tw.possibly_sensitive FROM twitter tw, twitter_users tu " \
      "WHERE tu.id_user = tw.id_user AND tw.params_query = '"
# ORDER BY tw.id"
# LIMIT 10

id = []
name = []
screen_name = []
created_at = []
id_tweet = []
id_tweet_origin = []
text_complete = []
hashtags = []
symbols = []
has_media = []
has_users_mention = []
has_urls_mention = []
source = []
in_reply_to_status_id = []
in_reply_to_user_id = []
in_reply_to_screen_name = []
contributors = []
is_quote_status = []
retweet_count = []
favorite_count = []
favorited = []
retweeted = []
possibly_sensitive = []
# lang = []

mycleantweet = ""
num = 1
tweet_list = []
new_tweet_list = []

if __name__ == '__main__':
    params_query = sys.argv[1]
    params_lang = sys.argv[2]

    fileCsvName = params_query+"_"+params_lang+"_twitter.csv"
    try:
        mypointer = basic.cnx.cursor()
        mypointer.execute(sql + params_query + "' AND tw.lang = '"+params_lang+"' ORDER BY tw.id")
        records = mypointer.fetchall()

        for row in records:
            id.append(row[0])
            name.append(row[1])
            screen_name.append(row[2])
            created_at.append(row[3])
            id_tweet.append(row[4])
            id_tweet_origin.append(row[5])
            mycleantweet = clean_text(row[6])
            #lower
            mycleantweet = str(mycleantweet).lower()
            # text_complete.append(row[6])
            text_complete.append(mycleantweet)
            hashtags.append(row[7])
            symbols.append(row[8])
            has_media.append(row[9])
            has_users_mention.append(row[10])
            has_urls_mention.append(row[11])
            source.append(row[12])
            in_reply_to_status_id.append(row[13])
            in_reply_to_user_id.append(row[14])
            in_reply_to_screen_name.append(row[15])
            contributors.append(row[16])
            is_quote_status.append(row[17])
            retweet_count.append(row[18])
            favorite_count.append(row[19])
            favorited.append(row[20])
            retweeted.append(row[21])
            possibly_sensitive.append(row[22])
            # lang.append(row[23])


            Twcsv = {'id': id, 'name': name, 'screen_name' : screen_name, 'created_at': created_at, 'id_tweet' : id_tweet,
                   'id_tweet_origin' : id_tweet_origin, 'text_complete':text_complete,'hashtags':hashtags,'symbols':symbols,
                   'has_media':has_media,'has_users_mention':has_users_mention,'has_urls_mention':has_urls_mention,
                   'source':source,'in_reply_to_status_id':in_reply_to_status_id,'in_reply_to_user_id':in_reply_to_user_id,
                   'in_reply_to_screen_name':in_reply_to_screen_name,'contributors':contributors,
                   'is_quote_status':is_quote_status,'retweet_count':retweet_count,'favorite_count':favorite_count,
                   'favorited':favorited,'retweeted':retweeted,'possibly_sensitive':possibly_sensitive}
                # ,'lang':lang}

            tw_cols = ['id','name','screen_name','created_at','id_tweet','id_tweet_origin','text_complete',
                    'hashtags','symbols','has_media','has_users_mention','has_urls_mention','source','in_reply_to_status_id',
                    'in_reply_to_user_id','in_reply_to_screen_name','contributors','is_quote_status','retweet_count',
                    'favorite_count','favorited','retweeted','possibly_sensitive']
                # ,'lang']


        df = DataFrame(Twcsv,columns = tw_cols)
        export_csv = df.to_csv(fileCsvName,index=None,header=True)
        print(df)

    except basic.Error as e:
        print("Error MySQL di: ", e)