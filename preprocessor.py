import re
import pandas as pd
from datetime import datetime





def preprocess(data):

    # pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[ap][m]\s-\s'
    # date_pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[ap][m]'

    # messages = re.split(pattern, data)[1:]
    # dates_pre = re.findall(date_pattern, data)

    # dates = []
    # for msg in dates_pre:
    #     date = re.sub(re.escape('\u202f'),' ', msg)
    #     dates.append(date)
        

    # Date=[]
    # f=1
    # if len(dates[0][7:dates[0].index(',')+1]) == 2:
    #     f=0
    #     for date in dates:
    #             timestamp = datetime.strptime(date, '%d/%m/%y, %I:%M %p')
    #             timestamp_formatted = timestamp.strftime('%d/%m/%y, %I:%M %p')
    #             Date.append(timestamp_formatted)
    # else:
    #     f=1
    #     for date in dates:
    #         timestamp = datetime.strptime(date, '%d/%m/%Y, %I:%M %p')
    #         timestamp_formatted = timestamp.strftime('%d/%m/%Y, %I:%M %p')
    #         Date.append(timestamp_formatted)

    # df = pd.DataFrame({'user_message': messages, 'message_date': Date})
    # # convert message_date type
    # if f == 0:
    #     df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')
    # else:
    #     df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')

    # df.rename(columns={'message_date': 'date'}, inplace=True)

    # users = []
    # messages = []
    # for message in df['user_message']:
    #     entry = re.split('([\w\W]+?):\s', message)
    #     if entry[1:]:  # user name
    #         users.append(entry[1])
    #         messages.append(" ".join(entry[2:]))
    #     else:
    #         users.append('group_notification')
    #         messages.append(entry[0])

    # df['user'] = users
    # df['message'] = messages
    # df.drop(columns=['user_message'], inplace=True)

    # df['only_date'] = df['date'].dt.date
    # df['year'] = df['date'].dt.year
    # df['month_num'] = df['date'].dt.month
    # df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day
    # df['day_name'] = df['date'].dt.day_name()
    # df['hour'] = df['date'].dt.hour
    # df['minute'] = df['date'].dt.minute

    # period = []
    # for hour in df[['day_name', 'hour']]['hour']:
    #     if hour == 23:
    #         period.append(str(hour) + "-" + str('00'))
    #     elif hour == 0:
    #         period.append(str('00') + "-" + str(hour + 1))
    #     else:
    #         period.append(str(hour) + "-" + str(hour + 1))

    # df['period'] = period

    pattern_24hr = '\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}\s-\s'
    pattern_12hr = '\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}\s[ap][m]\s-\s'
    pattern_yr = '\d{1,2}/\d{1,2}/\d{2},'

    match_12hr = re.search(pattern_12hr, data)
    match_24hr = re.search(pattern_24hr, data)
    pattern_year = re.search(pattern_yr,data)

    if match_12hr:
        current_time_pattern = '\d{1,2}:\d{1,2}\s[ap][m]'
        current_time_format = '%I:%M %p'
        if pattern_year:
            current_year_pattern = '\d{1,2}/\d{1,2}/\d{2}, '
            pattern = current_year_pattern+current_time_pattern+"\s-\s"
            current_date_format = '%d/%m/%y, '
            date_format = current_date_format+current_time_format
        else:
            current_year_pattern = '\d{1,2}/\d{1,2}/\d{4}, '
            pattern = current_year_pattern+current_time_pattern+"\s-\s"
            current_date_format = '%d/%m/%Y, '
            date_format = current_date_format+current_time_format
            
    elif match_24hr:
        current_time_pattern = '\d{1,2}:\d{1,2}'
        current_time_format = '%H:%M'
        if pattern_year:
            current_year_pattern = '\d{1,2}/\d{1,2}/\d{2}, '
            pattern = current_year_pattern+current_time_pattern+"\s-\s"
            current_date_format = '%d/%m/%y, '
            date_format = current_date_format+current_time_format
        else:
            current_year_pattern = '\d{1,2}/\d{1,2}/\d{4}, '
            pattern = current_year_pattern+current_time_pattern+"\s-\s"
            current_date_format = '%d/%m/%Y, '
            date_format = current_date_format+current_time_format
        
    date_pattern = current_year_pattern+current_time_pattern





    messages = re.split(pattern,data)[1:]

    dates_pre = re.findall(date_pattern, data)

    dates = []
    for msg in dates_pre:
        date = re.sub(re.escape('\u202f'),' ', msg)
        dates.append(date)
        

    Date=[]
    for date in dates:
            timestamp = datetime.strptime(date, date_format)
            timestamp_formatted = timestamp.strftime('%d/%m/%Y, %I:%M %p')
            Date.append(timestamp_formatted)
            

    df = pd.DataFrame({'user_message': messages, 'message_date': Date})
    # convert message_date type

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')


    df.rename(columns={'message_date': 'date'}, inplace=True)


    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period






    return df