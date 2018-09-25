import os
import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import pandas_datareader as pdr
import requests

app = dash.Dash(__name__)
server = app.server

app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H1('Portfolio Plotter'),
    html.H3(
    'Select tickers from dropdown below'
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['AMZN', 'SQ', 'LMT', 
        'AAPL', 'MJ', 'CGC', 'NFLX', 'TSLA', 'ZBRA', 'MU']],
        multi=True,
        className="twelve columns"
    ),
    html.Div([html.H3('Enter start & end dates:'),
        dcc.DatePickerRange(id='date_picker',
                        min_date_allowed = dt.datetime(2013,9,24),
                        max_date_allowed = dt.datetime.today(),
                        start_date = dt.datetime(2018, 1, 1),
                        end_date = dt.datetime.today()
                        )
				], 
                style={'display':'inline-block'}),

    html.H1(id='display_graphs2')
    ])


def get_company(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


@app.callback(dash.dependencies.Output('display_graphs2', 'children'),
              [dash.dependencies.Input('dropdown', 'value'),
              dash.dependencies.Input('date_picker', 'start_date'),
              dash.dependencies.Input('date_picker', 'end_date')])
def make_graphs(ticker_list, start_date, end_date):
    graph_list = []
    for ticker in ticker_list:
        start= start_date
        end= end_date
        # Needed to reset_index to make date back into a column header
        # Now this is indexed by an id number
        df = pdr.DataReader(ticker.upper(), 'iex', start, end).reset_index()
        graph_list.append(
        dcc.Graph(
            id=ticker,
            figure={
                'data':[
                    go.Candlestick(
                        x=df.date,
                        open=df.open,
                        high=df.high,
                        low=df.low,
                        close=df.close,
                        increasing=dict(line=dict(color= '#17BECF')),
                        decreasing=dict(line=dict(color= '#7F7F7F')))
                        ],
                'layout': go.Layout(
                    title=get_company(ticker) +' ('+ticker+')',
                    selectdirection='any',
                    titlefont=dict(size=40),
                    xaxis=dict(
                        title='Date',
                        linecolor='black',
                        linewidth=1,
                        mirror=True
                    ),
                    yaxis=dict(
                        title='Stock Price (USD)',
                        linecolor='black',
                        linewidth=1,
                        mirror=True
                    )
                )
            }
        ))
    return(graph_list)  

if __name__ == '__main__':
    app.run_server(debug=True)
