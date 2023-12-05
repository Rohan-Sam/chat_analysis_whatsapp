from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import warnings

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df =  df[df['user'] == selected_user]
    #Number of Messages
    num_messages =  df.shape[0]
    #Number of Words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    #Number of Media Messages
    media_messages =df[df['message'] == '<Media omitted>\n'].shape[0]

    #Number of Links Shared

    links = []

    extractor = URLExtract()

    for message in df['message']:
        links.extend(extractor.find_urls(message))

    
    num_links = len(links)


    return num_messages, len(words), media_messages, num_links



def most_busy_users(df):

    x = df['user'].value_counts().head()
    new_df=round((df['user'].value_counts().head()/df['message'].shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    new_df.index = new_df.index + 1
    return x,new_df

warnings.filterwarnings("ignore", category=pd.core.common.SettingWithCopyWarning)
def word_cloud_gen(selected_user,df):

    if selected_user != 'Overall':
        df =  df[df['user'] == selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']


    def remove_stop_words(message):
        y = []
        
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    wc_df = wc.generate(temp['message'].str.cat(sep=" "))

    return wc_df

def most_common_words(selected_user,df):

    if selected_user != 'Overall':
        df =  df[df['user'] == selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    wrd_df = pd.DataFrame(Counter(words).most_common(15))

    return wrd_df


def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df =  df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap