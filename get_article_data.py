import os
import requests
import psycopg2
import bs4
import datetime

from dotenv import load_dotenv #to remove for AWS


# scrap url details needed and return data
def get_article_data():
    # event, context
    response = requests.get("https://u.today/bitcoin-news")
    soup = bs4.BeautifulSoup(response.text, 'html.parser') 

    article_group = soup.select("div.category__news div.news__item")

    db_conn = os.getenv("DB_CONN")
    conn = psycopg2.connect(db_conn)
    cur = conn.cursor()

    cur.execute('''
        SELECT MAX(date)FROM utoday_article_data;
                    ''')
    last_utoday_article_date_PostgreSQL = cur.fetchall()
    cur.close()
    conn.close()

    # amend the format to be a single value and not a list of one tuple
    last_utoday_article_date_PostgreSQL_2=last_utoday_article_date_PostgreSQL[0][0]

    article_date_str = []
    for article in article_group:
        article_date_str.append(article.find('div', class_='humble').get_text())

    article_datetime = []
    for date_string in article_date_str:
        date_part = date_string.split(' - ')[0]
        time_part = date_string.split(' - ')[1]

        article_date = datetime.datetime.strptime(date_part, '%b %d, %Y').date()
        article_time = datetime.datetime.strptime(time_part, '%H:%M').time()
        combined_datetime = datetime.datetime.combine(article_date, article_time)
        article_datetime.append(combined_datetime)
    
    utoday_article_dates_to_append = [x for x in article_datetime if x > last_utoday_article_date_PostgreSQL_2]
    

    N=len(utoday_article_dates_to_append)

    article_datetime_str = [key.strftime("%Y-%m-%d, %H:%M") for key in utoday_article_dates_to_append]
    # print(article_datetime_str)

    article_url = []
    i = 0
    while i < N:
        article_url.append(article_group[i].find('a')['href'])
        i += 1 
    # print(article_url)

    article_title = []
    i = 0
    while i < N:
        # article_url.append(article_group[i].find('a')['href'])
        article_title.append(article_group[i].findChild('a').get_text().strip())
        i += 1 
    
    data_article_title=article_title
    return data_article_title
    print(data_article_title) # to remove for AWS
get_article_data() # to remove for AWS