import streamlit as st
import psycopg2
import os
import pandas as pd
from datetime import datetime
import time

# ###
# def set_theme():
#     st.session_state.theme = st.session_state.theme_option
# ###

# use the full width of the screen
st.set_page_config(layout="wide")

# CSS to reduce top margin even further
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0.99rem;  /* Adjust this value as needed */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ###
# if 'dark_mode' not in st.session_state:
#     st.session_state.dark_mode = False

# def toggle_theme():
#     st.session_state.dark_mode = not st.session_state.dark_mode
# ###

st.title("Bitcoin values & articles")















# retrieve bitcoin data from railways hosting PostgreSQL
def get_api_data():
    # dbconn = os.getenv("DB_CONN")
    dbconn = st.secrets["DB_CONN"]
    conn = psycopg2.connect(dbconn)
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM api_data ORDER BY date desc;
                ''')
    data = cur.fetchall()
    data_df=pd.DataFrame(data, columns=["date", "open", "high", "low", "close","volume"])
    return data_df # use these data outside the function
bitcoin_value=get_api_data()

#adjust date datatype
bitcoin_value["date"]=bitcoin_value["date"].astype(str)
bitcoin_value["date"]=pd.to_datetime(bitcoin_value["date"]).dt.date


# retrieve article data from railways hosting
# def get_article_data():
#     # dbconn = os.getenv("DB_CONN")
#     dbconn = st.secrets["DB_CONN"]
#     conn = psycopg2.connect(dbconn)
#     cur = conn.cursor()
#     cur.execute('''
#     SELECT * FROM article_data ORDER BY date desc;
#                 ''')
#     data_article = cur.fetchall()
#     data_article_df=pd.DataFrame(data_article, columns=["title", "url", "date"])
#     return data_article_df # use these data outside the function
# article_value=get_article_data()

# retrieve article data from railways hosting
def get_utoday_article_data():
    # dbconn = os.getenv("DB_CONN")
    dbconn = st.secrets["DB_CONN"]
    conn = psycopg2.connect(dbconn)
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM utoday_article_data ORDER BY date desc;
                ''')
    data_utoday_article = cur.fetchall()
    data_utoday_article_df=pd.DataFrame(data_utoday_article, columns=["title", "url", "date", "sentiment"])
    return data_utoday_article_df # use these data outside the function
utoday_article_value=get_utoday_article_data()


#create variable for latest date captured
latest_date=max(bitcoin_value["date"])


# create interactive text to show the latest data captured
_LOREM_IPSUM = f"the latest bitcoin values on {latest_date} are:"

Latest_Insight_values=bitcoin_value[(bitcoin_value["date"]==max(bitcoin_value["date"]))]
Latest_Insight_values_2=pd.DataFrame(Latest_Insight_values, columns=["open", "high", "low", "close","volume"])

def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)
    
    yield Latest_Insight_values_2


# create blocks to show buttons across the width of the screen
col1, col2 = st.columns(2)
with col1:
    if st.button("Latest insights, click here"):
        st.write_stream(stream_data)
with col2:
    if st.button("If you feel :rainbow[happy], click here!"):
        st.balloons()


# create variable for oldest/first date captured
oldest_date=min(bitcoin_value["date"])


# create a container with the filters
container = st.container(border=True)
col1, col2= container.columns(2)

all_values =["open", "high", "low", "close","volume"]
with col1:
    Date_range=st.slider("Select date range",value=[oldest_date,latest_date])
with col2:
    select_bitcoin_value = st.multiselect("Bitcoin Values", all_values, default=all_values)
        # rolling_average = st.toggle("Rolling average")


#create a slider to filter the date range
start_date, end_date = Date_range
filtered_data = bitcoin_value[(bitcoin_value['date'] >= start_date) & (bitcoin_value['date'] <= end_date)]


# adjust article list with url links being clickable
# article_value["url"] = article_value["url"].apply(lambda url: f'<a href="{url}" target="_blank">{url}</a>')

# adjust article list with url links being clickable
utoday_article_value["url"] = utoday_article_value["url"].apply(lambda url: f'<a href="{url}" target="_blank">{url}</a>')



# create multiple tabs to navigate across chart, data and article
tab1, tab2, tab3 = st.tabs(["📈 Chart", "🗃 Data", "📰 News"])
with tab1:
    st.subheader("Bitcoin chart")
    st.line_chart(
        filtered_data,
        x="date",
        y=select_bitcoin_value
    )

with tab2:
    # st.write("Content for Tab 2")
    st.subheader("Bitcoin data")
    st.dataframe(filtered_data, height=250, use_container_width=True)

# with tab3:
#     st.subheader("Bitcoin articles from Financial Times")
#     # Display DataFrame as HTML with clickable links in Tab 3
#     # st.markdown(df_articles.to_html(escape=False), unsafe_allow_html=True)
#         # Add CSS styling to control table height and width
#     bitcoin_article_table = f"""
#     <div style="overflow: auto; height: 250px; width: 100%;">
#         {article_value.to_html(escape=False, index=False)}
#     </div>
#     """
#     st.markdown(bitcoin_article_table, unsafe_allow_html=True)

with tab3:
    st.subheader("Bitcoin news from u.today")
    # Display DataFrame as HTML with clickable links in Tab 3
    # st.markdown(df_articles.to_html(escape=False), unsafe_allow_html=True)
        # Add CSS styling to control table height and width
    bitcoin_utoday_article_table = f"""
    <div style="overflow: auto; height: 250px; width: 100%;">
        {utoday_article_value.to_html(escape=False, index=False)}
    </div>
    """
    st.markdown(bitcoin_utoday_article_table, unsafe_allow_html=True)