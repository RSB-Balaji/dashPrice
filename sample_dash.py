from player import Player
from order import Order
from exchange import Exchange

import time

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

playerObj = Player('admin')
ex = Exchange('admin')

app.layout = html.Div([
    html.Table([
        html.Tr([
            html.Td([
                    html.Div([
                        dcc.Dropdown(
                            id='symbol-id',
                            options=[
                                {'label': 'MSFT', 'value': 'MSFT'},
                                {'label': 'TSLA', 'value': 'TSLA'},
                                {'label': 'AAPL', 'value': 'AAPL'}
                                    ],
                            style={'width':'100%'}
                            ),
                        ])
                    ]),

            html.Td([
                    html.Div([
                        dcc.RadioItems(
                            id='direction-id',
                            options=[
                                {'label':'BUY', 'value':'BUY'},
                                {'label':'SELL', 'value':'SELL'}],
                            labelStyle={'display':'inline-block'},
                            #style={"padding": "10px", "max-width": "800px", "margin": "auto"}
                            ),
                        ])
                    ]),

            html.Td([
                    html.Div([
                        dcc.RadioItems(
                            id='ordertype-id',
                            options=[
                                {'label':'Market Order', 'value':'MarketOrder'},
                                {'label':'Limit Order', 'value':'LimitOrder'}],
                            labelStyle={'display':'inline-block'},
                            #style={"padding": "10px", "max-width": "800px", "margin": "auto"}
                            ),
                        ])
                    ]),

            html.Td([
                    "Quantity:"
                ]),

            html.Td([
                    html.Div([
                        dcc.Input(
                            id='quantity-id',
                            type='number')
                        ])
                    ]),

            html.Td([
                "Limit Price:"
                ]),

            html.Td([
                    html.Div([
                        dcc.Input(id='price-id', type='text'),
                        ])
                    ]),

            html.Td([
                html.Button(id='sumbit-id', n_clicks=0, children='SUBMIT')
                ])

        ])
    ]),

    dcc.Graph(id='my-graph')
    #generate_table(df)
])

@app.callback(
    Output('my-graph', 'figure'), 
    [Input('sumbit-id', 'n_clicks'),
     Input('symbol-id', 'value'),
     Input('direction-id', 'value'),
     Input('ordertype-id', 'value'),
     Input('quantity-id', 'value'),
     Input('price-id', 'value')]
    )

def update_graph(n_clicks, symbol_value, direction_value, ordertype_value, quantity_value, price_value, playerObj=playerObj):
    AAPL = pd.DataFrame(ex.get_trade_prices('AAPL'), columns = ['Prices',])
    MSFT = pd.DataFrame(ex.get_trade_prices('MSFT'), columns = ['Prices',])
    TSLA = pd.DataFrame(ex.get_trade_prices('TSLA'), columns = ['Prices',])

    if symbol_value != None and direction_value != None and ordertype_value != None and quantity_value != None and price_value != None:
        try:
            order = Order(symbol_value, direction_value, quantity_value, price_value)
            playerObj.send_order_to_exchange(order)
        except Exception as e:
            print("Error sending order to exchange")
            print(e)

    return {
        'data': [{
            'x': locals()[symbol_value].index,
            'y': locals()[symbol_value]['Prices']
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }

if __name__ == '__main__':
    app.run_server()