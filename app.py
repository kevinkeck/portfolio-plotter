import os

import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)
server = app.server

app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H2(
    'Who\'s better? Karissa or Kevin?\nPlease select your answer from below'
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['Kevin', 'Kevin']],
        value='Select an answer'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
