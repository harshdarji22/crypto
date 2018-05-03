import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import mysql.connector
from datetime import datetime as dt
import statistics
import urllib.request
from bs4 import BeautifulSoup
from goose3 import Goose
import statistics
from sklearn.metrics import mean_squared_error
import csv

def get_ch(v):
	ch=[]
	for i in range(-1,-100,-1):
		ch.append(((v[i]-v[i-1])/v[i-1])*100)
	return ch
	
def get_opp_trends(b,v):
	sum=0
	for i in range(len(b)):
		if(b[i]*v[i]<0):
			sum=sum+1
	return (sum/len(b))*100

cnx = mysql.connector.connect(user='student', password='cs336student',
                              host='cs336.ckksjtjg2jto.us-east-2.rds.amazonaws.com',
                              database='CryptoNews')
							  


import csv

curr = pd.read_sql("select distinct currency_name from CryptoNews.Value",cnx)
currency = curr.iloc[:,0].values.tolist()

#print(currency)

bit_values_df = pd.read_sql("select quote from CryptoNews.Value where currency_name='Bitcoin'",cnx)
bit_values =  bit_values_df.iloc[:,0].values.tolist()
bit_ch = get_ch(bit_values)
print(len(bit_values))
#leng = []
final = [["Crypto Currency","Volatility","Mean Square Error","Opposite Trend %","Outlier Score"]]
for i in currency:
	val_temp_df = pd.read_sql("select quote from CryptoNews.Value where currency_name='"+i+"'",cnx)
	val_temp =  val_temp_df.iloc[:,0].values.tolist()
	if(len(val_temp)<101):
		continue
	ch =get_ch(val_temp)
	temp =[]
	std = statistics.stdev(ch)
	mse = mean_squared_error(bit_ch, ch)
	opp = get_opp_trends(bit_ch,ch)
	temp.append(i)
	temp.append(std)
	temp.append(mse)
	temp.append(opp)
	score = (std*0.1)+(mse*0.45)+(opp*0.45)
	temp.append(score)
	print(temp)
	final.append(temp)
	#leng.append(len(val_temp))

#print(sum(leng)/len(leng))
with open("outlier.csv", 'w', newline ='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for i in final:
        wr.writerow(i)
print("Output generated in outlier.csv")