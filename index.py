import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import mysql.connector
from datetime import datetime as dt
import statistics
import csv
import re
import dash_table_experiments as dte
from dash.dependencies import Input, Output, State
import plotly
import urllib.request
from bs4 import BeautifulSoup
from goose3 import Goose

from coinmarketcap import Market
coinmarketcap = Market()
stat = coinmarketcap.ticker(start=0, limit=10)
pv=[]
pl=[]
pv2=[]
for i in stat:
	pl.append(i['id'])
	pv.append(i['market_cap_usd'])
#print(stat[0]['id'])
#print(pv)
stat1 = coinmarketcap.stats()
bitcoin_per = stat1['bitcoin_percentage_of_market_cap']
#print(bitcoin_per)
bit = coinmarketcap.ticker('bitcoin')
bit_p = bit[0]['market_cap_usd']
#print(bit_p)

#print(pv[0].type)

for j in range(len(pv)):
	#print(pv[j])
	pv2.append((float(pv[j])*float(bitcoin_per))/float(bit_p))

pl.append("Others")	
pv2.append(100-sum(pv2))	

#print(pv2)

g = Goose()

def str_rep(s):
	f = False
	s1=""
	for i in s:
		if(i=='['):
			f = True
			continue
		if(i==']'):
			f = False
			continue
		if(f):
			continue
		s1 = s1+i
		
	return s1

def get_ch(v):
	ch=[]
	for i in range(-1,-100,-1):
		ch.append(((v[i]-v[i-1])/v[i-1])*100)
	return ch

curr_price = 0
curr_7_avg = 0
curr_30_avg = 0
change_7 = 0
change_30 =0

outlier_df1 = pd.read_csv("outlier.csv")
outlier_df1.sort_values(by=['Outlier Score'])
outlier_df = outlier_df1.iloc[61:161,:]

cnx = mysql.connector.connect(user='student', password='cs336student',
                              host='cs336.ckksjtjg2jto.us-east-2.rds.amazonaws.com',
                              database='CryptoNews')
							  

def takeSixth(elem):
    return elem[5]

def takeSecond(elem):
    return int(elem[1])

							  
							  
app = dash.Dash()
server = app.server
app.config['suppress_callback_exceptions']=True
#url("")
#application layout
app.layout = html.Div(style={'backgroundImage':'url("http://www.designbolts.com/wp-content/uploads/2013/02/Golf-Shirt-Grey-Seamless-Pattern-For-Website-Background.jpg")','width':'96%','margin':'0% 0% 0% 2%','borderRadius':'10px'},children=[
    html.H1(style={'textAlign':'center','font':'bold 35px Castellar, serif','padding':'20px 0px 0px 0px'} ,children='Crypto Analysis'),

	html.Label(style={'margin': '0% 0% 0% 1%','font':'25px Britannic, serif'},children='Select a currency:'),
	html.Br(),
	html.Div(style={'width':'20%','font-size':'25px','margin':'0% 0% 0% 1%'},children=dcc.Dropdown(
		#style={'font':'25px'}
		id='cryptos',
		options=[{'label':'Bitcoin', 'value':'Bitcoin',},
		{'label':'Ethereum', 'value':'Ethereum'},
		{'label':'Ripple', 'value':'Ripple',},
		{'label':'Litecoin', 'value':'Litecoin'},
		{'label':'Monero', 'value':'Monero'}],
		value = 'Bitcoin'
	)),
	#html.Div(children=html.Div(id='about')),
	html.Hr(),
	html.Div(style={'margin':'0% 0% 0% 1%'},children=[
        html.Div([
            html.H3(style={'font-weight':'bold','border': '2px solid black',},children='Price Chart'),
            html.Div(id='price',children=[])
        ], className="six columns"),

        html.Div([html.Div(style={'width':'20%','margin':'0% 0% 0% 2%'} ,children=[
            html.H3(style={'font-weight':'bold','border': '2px solid black'},children='Facts'),
            html.Div(style={'font-size':'20px','text-align': 'justify'},id='price_facts')
        ], className="six columns"),

        html.Div(style={'width':'26%','margin':'0% 0% 0% 2%'},children=[
            html.H3(style={'font-weight':'bold','border': '2px solid black',},children='About'),
            html.Div(style={'font-size':'20px','text-align': 'justify','height':'400px','overflow':'scroll'},id='about')
        ], className="six columns"),
    ], className="row"),
    ], className="row"),
	html.Hr(),
	html.Div([
        html.Div(style={'width':'30%','margin':'0% 0% 0% 1%'} ,children=[
            html.H3(style={'font-weight':'bold','border': '2px solid black'},children='Top News'),
            html.Div(style={'font-size':'20px',},id='top_news')
        ], className="six columns"),

        html.Div(style={'width':'20%','margin':'0% 0% 0% 2%'} ,children=[
            html.H3(style={'font-weight':'bold','border': '2px solid black'},children='Relevent Domains'),
            html.Div(style={'font-size':'20px',},id='rel_domains')
        ], className="six columns"),
		
		html.Div(style={'width':'43%','margin':'0% 0% 0% 2%'} ,children=[
            html.H3(style={'font-weight':'bold','border': '2px solid black'},children='Market Cap Distribution'),
            dcc.Graph(
				id='pi',
				figure={
					'data': [
						{'values': pv2, 'labels':pl , 'type': 'pie'},
					],
					'layout': {
						'title': "Market Cap Distribution",
						#'plot_bgcolor': '#eeeeee',
						#'paper_bgcolor': '#eeeeee',
					}
				}
			)
        ], className="six columns"),
    ], className="row"),
	html.Hr(),
	#html.Div(children=html.Div(id='price')),
	html.H1(style={'textAlign':'center','font':'bold 35px Castellar, serif','padding':'20px 0px 0px 0px'} ,children='Outlier Analysis'),
	html.Div([
    		html.Div(style={'margin':'0% 0% 0% 1%','width':'45%'},children = [
			html.H3(style={'font-weight':'bold','border': '2px solid black'},children='Outlier Feature Calculation'),
			dte.DataTable(
			rows=outlier_df.to_dict('records'),

			# optional - sets the order of columns
			#columns=sorted(outlier_df.columns),

			row_selectable=True,
			filterable=True,
			sortable=True,
			selected_row_indices=[],
			id='outlier'
		),
		html.Div(children=['''
		*All calculations are with respect to Bitcoin.
			
		''']),
		html.Div(style={'font-size':'20px',},children=['''
				
		This is a interactive table. You can sort, search and filter using any column in the table. The adjacent graphs will update accordingly.
		
		''']),],className="six columns"),
		html.Div([html.Div(id='selected-indexes'),
		dcc.Graph(
			id='graph-outlier'
		)],className="six columns"),
	], className="row"),
	html.Hr(),
	html.H1(style={'textAlign':'center','font':'bold 35px Castellar, serif','padding':'20px 0px 0px 0px'} ,children='Pump and Dump Analysis'),
	html.Div(style={'font-size':'20px',},children=['''
				
		Click on the below link to go to the pump and dump webpage
		
		''']),
	html.Div(style={'font-size':'30px'},children=html.A(href="https://blooming-woodland-80837.herokuapp.com/",target = "_blank", children = "Click here")),
	html.Div(style={'width':'95%','margin':'1% 2.5% 1% 2.5%','borderRadius':'10px','opacity':'1'}, children=html.Div(id='output')),
	
	

])





@app.callback(
    dash.dependencies.Output('about', 'children'),
    [dash.dependencies.Input('cryptos', 'value')])
	
def update_output(value):
	#global col
	#col = '{}'.format(value)
	BASE_URL = 'https://en.wikipedia.org/wiki/'
	BACK_URL = '{}'.format(value)
	if BACK_URL=="Ripple":
		BACK_URL = "Ripple_(payment_protocol)"
	if BACK_URL=="EOS":
		BACK_URL = "EOS.IO"
	if BACK_URL=="Monero":
		BACK_URL = "Monero_(cryptocurrency)"
	LANDING_PAGE = BASE_URL + BACK_URL
	f=g.extract(url = LANDING_PAGE)
	c = f.cleaned_text.split("\n")
	s = str_rep(c[0]+c[2])
	return s

@app.callback(
    dash.dependencies.Output('price', 'children'),
    [dash.dependencies.Input('cryptos', 'value')])
	
def update_output(value):
	#global col
	crypto = '{}'.format(value)
	hist=pd.read_sql("select quote, time from CryptoNews.Value where currency_name like '"+crypto+"'",cnx)
	
	p = hist.iloc[:,1].tolist()
	y = hist.iloc[:,0].tolist()
	
	q=[]
	ye=[]
	
	for i in range(0,len(y)-7):
		ye.append(p[i+7])
		temp = sum(y[i:i+7])/7
		q.append(temp)
		
	q2=[]
	ye2=[]
	
	global change_7
	change_7 = ((y[-1]-y[-8])/y[-8])*100
	
	global change_30
	change_30 = ((y[-1]-y[-31])/y[-31])*100
	
	
	global curr_price
	curr_price=y[-1]
	
	global curr_7_avg
	curr_7_avg=q[-1]
	
	
	
	
	for i in range(0,len(y)-30):
		ye2.append(p[i+30])
		temp = sum(y[i:i+30])/30
		q2.append(temp)
		
	global curr_30_avg
	curr_30_avg=q2[-1]
	
	
	
	x = html.Div(children=[dcc.Graph(
				id='pi',
				figure={
					'data': [
						{'x': p , 'y': y, 'type': 'line', 'name': 'Price','mode':'lines+markers'},
						{'x': ye , 'y': q, 'type': 'line', 'name': '7 Day moving Average','mode':'lines'},
						{'x': ye2 , 'y': q2, 'type': 'line', 'name': '30 Day moving Average','mode':'lines'}
					],
					'layout': {
						'title': crypto+' price',
						#'plot_bgcolor': '#eeeeee',
						#'paper_bgcolor': '#eeeeee',
					}
				}
			)])
	
	return x
	
@app.callback(
    dash.dependencies.Output('price_facts', 'children'),
    [dash.dependencies.Input('price', 'children')])
	
def update_output(value):
	#global col
	#col = '{}'.format(value)
	
	
	
	x = html.Table(
		[
			html.Tr( [html.Td("Current Price"), html.Td(round(curr_price,2))] ),
			html.Tr( [html.Td("Past 7 days Average"), html.Td(round(curr_7_avg,2))] ),
			html.Tr( [html.Td("Past 30 days Average"), html.Td(round(curr_30_avg,2))] ),
			html.Tr( [html.Td("Past 7 days % Change"), html.Td(round(change_7,2))] ),
			html.Tr( [html.Td("Past 30 days % Change"), html.Td(round(change_30,2))] )
			
		]
)
	return x

import csv
	
@app.callback(
    dash.dependencies.Output('rel_domains', 'children'),
    [dash.dependencies.Input('cryptos', 'value')])
	
def update_output(value):
	#global col
	#col = '{}'.format(value)
	c = '{}'.format(value)
	f = "dom_"+c+".csv"
	reader2 = csv.reader(open(f),delimiter=',')
		
	#final = []
		
	doms = sorted(reader2, key=takeSecond, reverse = True)
	dom = list(doms)
	links = []
	for i in dom:
		links.append("http://"+i[0])
	x = html.Table(
		[
			html.Tr( [html.Td(html.A(href=links[0],target = "_blank", children = dom[0][0]))]),
			html.Tr( [html.Td(html.A(href=links[1],target = "_blank", children = dom[1][0]))]),
			html.Tr( [html.Td(html.A(href=links[2],target = "_blank", children = dom[2][0]))]),
			html.Tr( [html.Td(html.A(href=links[3],target = "_blank", children = dom[3][0]))]),
			html.Tr( [html.Td(html.A(href=links[4],target = "_blank", children = dom[4][0]))]),
			
		]
)
	return x
	
	
@app.callback(
    dash.dependencies.Output('top_news', 'children'),
    [dash.dependencies.Input('cryptos', 'value')])
	
def update_output(value):
	#global col
	#col = '{}'.format(value)
	
	c = '{}'.format(value)
	f = "dom_"+c+".csv"
	reader2 = csv.reader(open(f),delimiter=',')
		
	final = []
		
	doms = sorted(reader2, key=takeSecond, reverse = True)
	dom = list(doms)
	print(len(dom))
	i=0
	j=0
	#for i in range(5):
	while(i<5):
		d = dom[j][0]
		print(d)
		out =[]
		reader = csv.reader(open("output.csv"),delimiter=',')
		filtered = filter(lambda p:p[0]==c, reader)
		fil = filter(lambda p: re.search("//.*?/",p[1]).group() == "//"+d+"/",filtered)
		fil2 = filter(lambda p:p[4]=="Y", fil)
		sortedList = sorted(fil2, key=takeSixth, reverse = True)
		out = list(sortedList)
		for i in sortedList:
			print("a")
		#	out.append(i)
		j=j+1
		try:
			
			final.append(out[0])
			print(out[0][2])
			i=i+1
		except:
			continue
	x = html.Table(
		[
			html.Tr( [html.Td(html.A(href=final[0][1],target = "_blank", children = final[0][2]))]),
			html.Tr( [html.Td(html.A(href=final[1][1],target = "_blank", children = final[1][2]))]),
			html.Tr( [html.Td(html.A(href=final[2][1],target = "_blank", children = final[2][2]))]),
			html.Tr( [html.Td(html.A(href=final[3][1],target = "_blank", children = final[3][2]))]),
			html.Tr( [html.Td(html.A(href=final[4][1],target = "_blank", children = final[4][2]))]),	
		])
	return x

	
@app.callback(
    Output('outlier', 'selected_row_indices'),
    [Input('graph-outlier', 'clickData')],
    [State('outlier', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices
	



@app.callback(
    Output('graph-outlier', 'figure'),
    [Input('outlier', 'rows'),
     Input('outlier', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('Opposite Trends', 'Mean Square Error','Volatility', ),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['Crypto Currency'],
        'y': dff['Opposite Trend %'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['Crypto Currency'],
        'y': dff['Mean Square Error'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['Crypto Currency'],
        'y': dff['Volatility'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis2']['type'] = 'log'
    fig['layout']['yaxis3']['type'] = 'log'
    return fig
	


# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})
	
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
	
if __name__ == '__main__':
    app.run_server(debug=True)
