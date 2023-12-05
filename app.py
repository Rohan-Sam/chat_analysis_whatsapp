import streamlit as st
import preprocessor
import pandas as pd
import helper
from matplotlib import pyplot as plt
import seaborn as sns
import warnings


warnings.filterwarnings("ignore", category=UserWarning, message="Glyph.*missing from current font.")


st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    st.dataframe(df)


    if st.sidebar.button("Show Analysis"):
        
        num_messages, num_words, media_messages, num_links = helper.fetch_stats(selected_user,df)
        

        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.header("Total Messsages")
            st.title(num_messages)
            

        with col2:
            st.header("Total Words")
            st.title(num_words)
            

        with col3:
            st.header("Media Messages")
            st.title(media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        # plt.setp(ax.get_xticklabels(), rotation=90, ha='right')
        ax.set_xticks(ax.get_xticks()[::2])
        st.pyplot(fig)


        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        #Most Busy users
        if selected_user == 'Overall':

            st.header("Most Busy User:")

            x, new_df = helper.most_busy_users(df)

            fig , ax = plt.subplots()
            
            


            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        #WordCloud
        st.header("WordCloud:")
        df_wc = helper.word_cloud_gen(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #Common Words

        st.header("Most Common Words:")

        wrd_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(wrd_df[0],wrd_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Emoji
        st.header("Emoji Counts:")
        emoji_df = helper.emoji_helper(selected_user,df)

        col1, col2 = st.columns(2)


        with col1:

            st.dataframe(emoji_df)

        with col2:

            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
