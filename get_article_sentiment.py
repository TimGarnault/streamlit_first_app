
from dotenv import load_dotenv #to remove for AWS
import os
import requests


# get article title and assign a sentiment
def get_article_sentiment():
    # event, context
    load_dotenv()
    # article_title=event["responsePayload"]
    article_title=['ETH/BTC Somehow Keeps Plunging Even Lower', 'Strategy on Cusp of Losing All Its Bitcoin Gains', 'Binance CEO Says Tariff Mayhem May Benefit Crypto', "Mega USDT Transfer Worth $400,000,000 Stuns World's Largest Crypto Exchange", 'Ripple CTO Responds to New Satoshi Nakamoto Identity Rumors', 'Binance Delists 14 Coins in One Blow: Market Reacts', 'Schiff Agrees with Saylor’s Bitcoin Take', "Satoshi's Portfolio Collapses by $30 Billion", 'Breaking: XRP Collapses 8% in Minutes Because of This One Word']
    api_key = os.getenv("HF_API_KEY")
    url = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
    headers = { "Authorization": f"Bearer {api_key}" }
    payload = { "inputs": article_title } # "inputs" will accept single string or list of strings
    response = requests.post(url, headers=headers, json=payload)
    sentiment_response=response.json()
    N=len(sentiment_response)
    sentiment_analysis_rows_to_append=[]
    
    i = 0
    while i < N:
        sentiment_analysis_rows_to_append.append(list(sentiment_response[i][0].items())[0][1])   
        i += 1    
    return sentiment_analysis_rows_to_append
    print(sentiment_analysis_rows_to_append) # to remove for AWS
get_article_sentiment() # to remove for AWS
