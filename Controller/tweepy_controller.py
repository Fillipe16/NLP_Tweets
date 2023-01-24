# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 19:32:50 2023

@author: Fellipe
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 10:44:53 2022

@author: Fellipe
"""
import sys



import tweepy
import requests

import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession,Row 
from pyspark.sql.functions import col, udf

import datetime
import pytz
import json
from decouple import config

path = config("path_folder")
if(path not in sys.path):
    sys.path.append(path)
    
from Model.tweet_model import Tweet
from Controller.model_controller import model_ml

CONFIG_DIR=config('CONFIG_DIR')
BEARER_TOKEN=config('BEARER_TOKEN')
url_ts = config('url_ts')
url_bar = config('url_bar')
url_stats = config('url_stats')

def get_sparkSession():
    spark = SparkSession \
          .builder \
          .appName("PostgreSQL Connection") \
          .config("spark.jars", CONFIG_DIR) \
          .getOrCreate()
    sc=spark.sparkContext
    sc.setLogLevel("ERROR")
    return spark

def post_request(url,data):
    headers = { "Content-Type": "application/json"}
    
    try:
        response1 = requests.request(method="POST",url=url[0], headers=headers,data=data[0])
        response2 = requests.request(method="POST",url=url[1], headers=headers,data=data[1])
        response3 = requests.request(method="POST",url=url[2], headers=headers,data=data[2])
    except:
        print("Ocorreu um erro no método POST")
        
def run_udf(tweet_obj,df_bar,df_stats,spark):
   
    temporal_data = [{'date':tweet_obj.date,'sentiment':tweet_obj.sentiment_label}]
    bar_data = df_bar.toJSON().map(lambda j: json.loads(j)).collect()
    stats_data = df_stats.toJSON().map(lambda j: json.loads(j)).collect()
    data_list = [temporal_data,bar_data,stats_data]
    
    url = [url_ts,url_bar,url_stats] 
   
    data = [json.dumps(d,cls=DateTimeEncoder) for d in data_list]
    # Inserir URL nos cols, cada url vai ta associada a um push dataset
    cols = Row("url","data")

    udf_api = udf(post_request)
    request_df = spark.createDataFrame([cols(url,data)])
    
    result_df = request_df \
         .withColumn("result", udf_api(col("url"),col("data"))) \
         .show(truncate=False)
        
    return None

def clean_rules(streaming_client):
    rules = streaming_client.get_rules()[0]
    try:
        ids = [rules[i][2] for i in range(len(rules))]
        streaming_client.delete_rules(ids)
        return None
    except:
        return None
    
class DateTimeEncoder(json.JSONEncoder):

        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
            
class get_tweets(tweepy.StreamingClient):
    
    def __init__(self, bearer_token,spark):
        tweepy.StreamingClient.__init__(self,bearer_token)
        self.spark = spark
        
    def on_tweet(self, tweet):
        
        sentiment_dict = {'LABEL_0':"Negativo", "LABEL_1":"Neutro", "LABEL_2":"Positivo"}
        
        tweet_id = tweet.id
        tweet_text = tweet.text 
        
        clean_text = model_ml.preprocessing_text(tweet_text)
        
        pred = model_ml.sentiment_prediction(tweet_text)
        
        sentiment = sentiment_dict[pred[0]['label']]
        sentiment_label = int(pred[0]['label'][-1])
        confidence = float(pred[0]['score'])
        date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
        
        tweet_obj = Tweet(tweet_id,clean_text,date,sentiment,sentiment_label,confidence)
        
        # Inserindo os dados brutos no postgreSQL
        tweet_obj.insert(self.spark)
        
        # Selecionando os dados para os gráficos
        df_bar,df_stats = tweet_obj.select(self.spark)
    
        run_udf(tweet_obj,df_bar,df_stats,self.spark)
        
        return 0
    
def main():
    spark = get_sparkSession()
    Tweet.getConnection(spark)
    
    streaming_client = get_tweets(BEARER_TOKEN,spark)
    
    clean_rules(streaming_client)
    
    streaming_client.add_rules([tweepy.StreamRule("#MondayMotivation lang:en")])
    streaming_client.filter()

if __name__ == "__main__":
    
    
    main()


