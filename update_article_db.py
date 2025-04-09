import pandas as pd
from datetime import datetime

from dotenv import load_dotenv
import os


import psycopg2

def update_article_db():
    Article_df = pd.DataFrame({
    "title": article_title,
    "url": article_url,
    "date": article_datetime_str,
    "sentiment":sentiment_analysis_rows_to_append
    })
    article_data_multiple_rows = list(Article_df.itertuples(index=False, name=None))
    conn = psycopg2.connect(db_conn)
    cur = conn.cursor()

    cur.executemany(
    '''
    INSERT INTO utoday_article_data(title, url, date, sentiment)
    VALUES (%s, %s, %s, %s);
    ''', article_data_multiple_rows)

    conn.commit()

    cur.close()
    conn.close()

    print(Article_df) # to remove for AWS
update_article_db() # to remove for AWS