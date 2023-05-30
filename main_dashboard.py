"""
Example copied from https://stackoverflow.com/questions/63589249/plotly-dash-display-real-time-data-in-smooth-animation
"""
# Standard libraries
# Third party libraries
import pandas as pd
import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from jupyter_dash import JupyterDash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
# Custom libraries
from ping_classes.pingmanager import PingManager

# Configuration
pd.options.plotting.backend = "plotly"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialization
ping_manager = PingManager("config.yaml")
ping_manager.start()
df = ping_manager.target_deque

# plotly figure
fig = df.plot(template='plotly_dark')

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(style={'backgroundColor': '#111111'},
                      children=[
                          html.H1(children="Ping to target [ms]",
                                  style={'textAlign': 'center',
                                         'color': '#FFFFFF'}),
                          dcc.Interval(
                              id='interval-component',
                              interval=1 * 2050,  # in milliseconds
                              n_intervals=0
                          ),
                          dcc.Graph(id='graph'),
                          html.Button('Submit', id='button-example-1'),
                          html.Div(id='output-container-button',
                                   children='Enter a value and press submit',
                                   style={'color': '#FFFFFF'})
                      ])


# Define callback to update graph
@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='interval-component', component_property="n_intervals")]
)
def streamFig(value):
    global df
    df = ping_manager.target_deque
    fig = df.plot(template='plotly_dark')
    fig.update_layout(
        xaxis_title="Samples [-]",
        yaxis_title="Ping [ms]",
    )
    return fig


@app.callback(
    Output(component_id='output-container-button', component_property='children'),
    [Input(component_id='button-example-1', component_property='n_clicks')],
    [State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


app.run_server(host="0.0.0.0", port=8069, dev_tools_ui=True,  # debug=True,
               dev_tools_hot_reload=True, threaded=True)
