import pandas as pd
import numpy as np
import calendar
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from api import 

meses=list(calendar.month_name)[1:]

def limpiar_fechas(fecha):
    fecha=fecha.strip("Posted ").split(" ")
    for i in range(0,len(meses)):
        if fecha[0] in meses[i]:
            month=str(i+1)
            if len(month)==1:
                month="0"+month
    fecha[1]=fecha[1].strip(".").strip(",")
    if len(fecha[1])==1:
        fecha[1]="0"+fecha[1]
    if len(fecha)==3:
        fecha[2]=fecha[2].strip().strip(".")
        res=fecha[1]+"/"+month+"/"+fecha[2]
    elif len(fecha)==2:
         res="Unknow"
        
    return res

def es_nulo(string):
    if str(string)==str(np.nan):
         return "nulo"
    else:
         return string

def polaridad(indice):
    if indice>-1 and indice<(2/3-1):
        return 0
    elif indice>(2/3-1) and indice<(1-2/3):
        return 1
    elif indice>(1-2/3) and indice<1:
        return 2
    else:
        return 1

def aplicar_nlp(text):
    return polaridad(sia.polarity_scores(text)["compound"])
    
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

nombre="datasets/user_reviews.csv"

df=pd.read_csv(nombre,sep=";")

#print(df.isna().sum())
#print(df.isna().mean())

df["posted"].fillna("Unknow",inplace=True)

df["posted"]=df["posted"].apply(lambda x:limpiar_fechas(x))

df["review"].fillna("Unknow",inplace=True)
df["sentiment_analysis"]=df["review"].apply(lambda x:aplicar_nlp(x))

df.drop(["review"],axis=1,inplace=True)

#print(df.isna().sum())
#print(df.isna().mean())

print("\nguardando....")
df.to_csv(nombre,sep=";",index=False)