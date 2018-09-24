import os
import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import pandas_datareader as pdr


app = dash.Dash(__name__)
server = app.server

app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H1('Portfolio Plotter'),
    html.H2(
    'Select tickers from dropdown below'
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['AMZN', 'SQ', 'LMT', 
        'AAPL', 'MJ', 'CGC', 'NFLX', 'TSLA', 'ZBRA', 'MU']],
        multi=True,
        value=['AMZN']
    ),        
    html.Div([html.H3('Enter start & end dates:'),
    dcc.DatePickerRange(id='date_picker',
                        min_date_allowed = dt.datetime(2015,1,1),
                        max_date_allowed = dt.datetime.today(),
                        start_date = dt.datetime(2018, 9, 1),
                        end_date = dt.datetime.today()
					)
				], style={'display':'inline-block'}),
    html.Div(id='display_value')
    ])


@app.callback(dash.dependencies.Output('display_value', 'children'),
              [dash.dependencies.Input('dropdown', 'value'),
              dash.dependencies.Input('date_picker', 'start_date'),
              dash.dependencies.Input('date_picker', 'end_date')])
def make_dataframe(ticker_list, start_date, end_date):
    # I need to change this to make multiple dataframes. 1 for each ticker.
    graph_list = []
    for ticker in ticker_list:
        start= start_date
        end= end_date
        #end = dt.datetime.today()
        #start = dt.datetime(2018,1,1)
        # Needed to reset_index to make date back into a column header
        # Now this is indexed by an id number
        df = pdr.DataReader(ticker.upper(), 'iex', start, end).reset_index()
        graph_list.append(dcc.Graph(
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
                        ]
                        }
        ))
    print(graph_list)
    return(graph_list)
        # I could make a graph using the same function
        # updated graphs should replace old graphs. 
        # and when a ticker is removed, the graph should be removed    

if __name__ == '__main__':
    app.run_server(debug=True)
