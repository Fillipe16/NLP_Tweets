# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from decouple import config

USER_BD = config('USER_BD')
PASSWORD_BD = config('PASSWORD_BD')

class Tweet():
    def __init__(self,id,text,date,sentiment_text, sentiment_label, confidence):
        self.id = id
        self.text = text
        self.date = date
        self.sentiment_text = sentiment_text
        self.sentiment_label = sentiment_label
        self.confidence = confidence
        
    def getConnection(spark):
        
        tb_tweets = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/Data_Analysis")\
        .option("dbtable", "twitter.\"TB_TWEETS\"") \
        .option("user", USER_BD) \
        .option("password", PASSWORD_BD) \
        .option("driver", "org.postgresql.Driver") \
        .load()

        tb_tweets.createOrReplaceTempView("tweets_df")
        
        return None
    
    def insert(self,spark):
        try:
            sql_insert = f"INSERT INTO tweets_df values ('{self.id}','{self.text}','{self.date}','{self.sentiment_text}',{self.confidence},{self.sentiment_label})"
            spark.sql(sql_insert)
        except:
            print("Não foi possivel inserir no BD")
        return None
    
    def select(self,spark):
        
        sql_bars = "select sentiment,count(id) as contagem from tweets_df group by sentiment"
        sql_stats = "select count(id) as contagem,avg(sentiment_label) as media,2 as media_max, 0 as media_min  from tweets_df"
        
        try:
            df_bars = spark.sql(sql_bars)
            df_stats = spark.sql(sql_stats)
            return [df_bars,df_stats]
        except:
            print("Não foi possivel fazer o select no BD")
            return None