import os

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas_datareader as pdr
from pandas_datareader.data import get_quote_yahoo

data = get_quote_yahoo('AMZN')
price = (data['price'])


app = dash.Dash(__name__)
server = app.server

app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H2(
    #'Select tickers from dropdown below'
    str(price)
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['AMZN', 'SQUARE', 'LMT', 
        'AAPL', 'MJ', 'CGC', 'ACBFF', 'NFLX', 'TESLA', 'ZBRA', 'MU']],
        multi=True,
        value=['AMZN', 'SQUARE', 'LMT', 
        'AAPL', 'MJ', 'CGC', 'ACBFF', 'NFLX', 'TESLA', 'ZBRA', 'MU']
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
# display the stock prices for all selected values 

if __name__ == '__main__':
    app.run_server(debug=True)
