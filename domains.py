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

g = Goose()

curr_price = 0
curr_7_avg = 0
curr_30_avg = 0

cnx = mysql.connector.connect(user='student', password='cs336student',
                              host='cs336.ckksjtjg2jto.us-east-2.rds.amazonaws.com',
                              database='CryptoNews')
							  


import csv

dom = []

with open('domains.csv', 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		dom.append(row[0])
		#print ', '.join(row)
	
#print(dom)
	
count = []

'''
count.append(['a',1])
count.append(['b',2])
count.append(['c',3])
count.append(['d',4])
count.append(['e',5])

with open("dom_bit.csv", 'w', newline ='') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for i in count:
		wr.writerow(i)


'''
'''	
for i in dom:
	temp = pd.read_sql("select count(*) from CryptoNews.cryptonews WHERE MATCH (content) AGAINST ('bitcoin' IN NATURAL LANGUAGE MODE) and link like '%"+i+"%'",cnx)
	#print(temp.iloc[:,0].tolist()[0])
	count.append([i,temp.iloc[:,0].tolist()[0]])
	#print(count)
	
with open("dom_Bitcoin.csv", 'w', newline ='') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #wr.writerows(count)
	for i in count:
		wr.writerow(i)
print("bitcoin done")		
count = []

	
for i in dom:
	temp = pd.read_sql("select count(*) from CryptoNews.cryptonews WHERE MATCH (content) AGAINST ('ethereum' IN NATURAL LANGUAGE MODE) and link like '%"+i+"%'",cnx)
	count.append([i,temp.iloc[:,0].tolist()[0]])
	
with open("dom_Ethereum.csv", 'w', newline ='') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #wr.writerows(count)
	for i in count:
		wr.writerow(i)
		
print("ethereum done")		
count = []

	
for i in dom:
	temp = pd.read_sql("select count(*) from CryptoNews.cryptonews WHERE MATCH (content) AGAINST ('ripple' IN NATURAL LANGUAGE MODE) and link like '%"+i+"%'",cnx)
	count.append([i,temp.iloc[:,0].tolist()[0]])
	
with open("dom_Ripple.csv", 'w', newline ='') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #wr.writerows(count)
	for i in count:
		wr.writerow(i)
		
print("ripple done")	
'''
	
count = []

'''	
for i in dom:
	temp = pd.read_sql("select count(*) from CryptoNews.cryptonews WHERE MATCH (content) AGAINST ('bitcoin cash' IN NATURAL LANGUAGE MODE) and link like '%"+i+"%'",cnx)
	count.append([i,temp.iloc[:,0].tolist()[0]])
	
with open("dom_bitc.csv", 'w', newline ='') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #wr.writerows(count)
	for i in count:
		wr.writerow(i)

print("bitcoin cash done")		
'''	
count = []

	
for i in dom:
	temp = pd.read_sql("select count(*) from CryptoNews.cryptonews WHERE MATCH (content) AGAINST ('eos' IN NATURAL LANGUAGE MODE) and link like '%"+i+"%'",cnx)
	count.append([i,temp.iloc[:,0].tolist()[0]])
	
with open("dom_EOS.csv", 'w', newline ='') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #wr.writerows(count)
	for i in count:
		wr.writerow(i)
		
print("eos done")		
count = []

	
for i in dom:
	temp = pd.read_sql("select count(*) from CryptoNews.cryptonews WHERE MATCH (content) AGAINST ('litecoin' IN NATURAL LANGUAGE MODE) and link like '%"+i+"%'",cnx)
	count.append([i,temp.iloc[:,0].tolist()[0]])
	
with open("dom_Litecoin.csv", 'w', newline ='') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #wr.writerows(count)
	for i in count:
		wr.writerow(i)
		
print("litecoin done")		
count = []

	
for i in dom:
	temp = pd.read_sql("select count(*) from CryptoNews.cryptonews WHERE MATCH (content) AGAINST ('monero' IN NATURAL LANGUAGE MODE) and link like '%"+i+"%'",cnx)
	count.append([i,temp.iloc[:,0].tolist()[0]])
	
with open("dom_Monero.csv", 'w', newline ='') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #wr.writerows(count)
	for i in count:
		wr.writerow(i)
print("monero done")
