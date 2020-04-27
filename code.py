import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import numpy as np
import random
from collections import deque

def Calculate_Price(mu, sigma, S0, t, seed):
    np.random.seed(seed)
    Z_sim = np.random.normal(size = t-1)    
    log_returns = []
    T = np.linspace(0., 1., t)
    for i in range(len(Z_sim)):
        log_returns.append(np.exp((mu-0.5*sigma**2)*T[i] + sigma*Z_sim[i]))
    cum_returns = [1]+list(np.cumprod(log_returns))
    sample_path = [S0*i for i in cum_returns]
    #plot
    # plt.plot(T, sample_path, 'b')
    # plt.title("Geometric Brownian motion mu:{} sigma:{}".format(mu, sigma))
    # plt.xlabel("Timesteps:{}".format(t))
    # plt.show(block=True)
    return sample_path

def seconds_to_hhmmss(seconds):
    hour = seconds//3600 
    minute = (seconds-hour*60)//60
    second = seconds-hour*60-minute*60
    hour+=9
    if hour+9 < 10:
        hour = str('0')+str(hour)
    else:
        hour = str(hour)
    if minute < 10:
        minute = str('0')+str(minute)
    else:
        minute = str(minute)
    if second < 10:
        second = str('0')+str(second)
    else:
        second = str(second)
    return hour+':'+minute+':'+second

n = 1000
Time = [seconds_to_hhmmss(i) for i in range(1,n+1)]
Prices = Calculate_Price(0.0003, 0.005, 100, n, 5)
Predicted_Prices = Calculate_Price(0.0005, 0.003, 100, n, 5)
P = deque(maxlen=1000)
PP = deque(maxlen=1000)
T = deque(maxlen=1000)
P.append(Prices[0])
T.append(Time[0])
PP.append(Predicted_Prices[0])
    
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000,
        )
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    T.extend(Time[len(T)+1 : len(T)+21])
    P.extend(Prices[len(P)+1 : len(P)+21])
    PP.extend(Predicted_Prices[len(PP)+1 : len(PP)+51])
    
    Original_Price_Figure = plotly.graph_objs.Scatter(
            x=list(T),
            y=list(P),
            name='Original Price',
            mode= 'lines+markers',
            # fill= 'tozeroy',
            )
    
    Predicted_Price_Figure = plotly.graph_objs.Scatter(
            x=list(T),
            y=list(PP),
            name='Predicted Price',
            mode= 'lines+markers',
            # fill= 'tozeroy',
            )
    
    data = [Original_Price_Figure , Predicted_Price_Figure]
    
    fig = {'data': data,'layout' : go.Layout(title={'text': "Stock Price", 'font':{'size' : 30, 'color':'#1e90ff'}},
                                                yaxis=dict(range=[min(Prices)-2,max(Prices)+2]),
                                                xaxis_title="Time (seconds)",
                                                yaxis_title="Price (Rupees)"
                                                )}
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)

