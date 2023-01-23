# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 19:52:17 2023

@author: Fellipe
"""
import re

from transformers import pipeline
from decouple import config

path_model = config('path_model')

class model_ml():
    
    def preprocessing_text(text):
        TROCAR_POR_ESPACO = re.compile('[/(){}\[\]\|@,;]')
        REMOVER = re.compile('[^0-9a-z #+_]')
        
        text = text.lower()
        text = re.sub('(http)\S*', '', text) # Retirando os hiperlinks
        text = re.sub('(rt)\s','', text) # Retirando a tag de Retweet
        text = re.sub('(@)\S*','', text) # Retirando para quem o Retweet foi feito
        text = re.sub('(#)\S*','', text) # Retirando hashtags
        text = REMOVER.sub('', text) 
        text = TROCAR_POR_ESPACO.sub(' ', text)
        text = re.sub('[0-9]', '', text)
        
        return text
    
    def sentiment_prediction(text):
        
        clf = pipeline("sentiment-analysis", model = path_model, tokenizer = path_model)
        
        predictions = clf.predict(text)
        return predictions
    