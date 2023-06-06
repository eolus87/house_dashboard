__author__ = "Nicolas Gutierrez"

# Standard libraries
# Third party libraries
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
# Custom libraries
from ping_classes.pingmanager import PingManager

# Configuration
pd.options.plotting.backend = "plotly"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Initialization
def target_deque_infrastructure(ping_manager: PingManager) -> pd.DataFrame:
    # infrastructure_df = ping_manager.target_deque.iloc[:, 0:3]
    infrastructure_df = ping_manager.target_deque.iloc[:, :]
    return infrastructure_df


def target_deque_personal_devices(ping_manager: PingManager) -> pd.DataFrame:
    infrastructure_df = ping_manager.target_deque.iloc[:, 3:]
    return infrastructure_df


def get_table():
    df = target_deque_personal_devices(ping_manager)
    devices_list = df.columns.to_list()
    mean_list = np.round(df.tail(10).mean()).to_list()
    std_list = np.round(df.tail(10).std()).to_list()
    at_home = []
    for x in mean_list:
        if x > 1000:
            at_home.append(False)
        else:
            at_home.append(True)

    data_as_dict = {"Devices": devices_list,
                    "Mean [ms]": mean_list,
                    "Std [ms]": std_list,
                    "At Home": at_home}
    data_as_pd = pd.DataFrame(data_as_dict)

    return data_as_pd


ping_manager = PingManager("config.yaml")
ping_manager.start()

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(style={'backgroundColor': '#111111'},
                      children=[
                          # Title and Infrastructure figure
                          html.H1(children="Infrastructure ping [ms]",
                                  style={'textAlign': 'center',
                                         'color': '#FFFFFF'}),
                          dcc.Interval(
                              id='interval_refresh',
                              interval=1 * 1050,  # in milliseconds
                              n_intervals=0
                          ),
                          dcc.Graph(id='infrastructure_graph'),
                          # Title and personal devices figure
                          html.H1(children="Personal devices ping [ms]",
                                  style={'textAlign': 'center',
                                         'color': '#FFFFFF'}),
                          html.Div(dash_table.DataTable(data=get_table().to_dict('records'),
                                                        columns=[{"name": i, "id": i} for i in get_table().columns],
                                                        id='tbl')),
                          # Button
                          html.Button('Submit', id='button-example-1'),
                          html.Div(id='output-container-button',
                                   children='Enter a value and press submit',
                                   style={'color': '#FFFFFF'})
                      ])


# Define callback to update graph
@app.callback(
    Output(component_id='infrastructure_graph', component_property='figure'),
    Input(component_id='interval_refresh', component_property="n_intervals")
)
def stream_fig(value):
    df = target_deque_infrastructure(ping_manager)
    fig = df.plot(template='plotly_dark')
    fig.update_layout(
        xaxis_title="Samples [-]",
        yaxis_title="Ping [ms]",
    )
    return fig


@app.callback(
    Output(component_id='tbl', component_property='data'),
    Input(component_id='interval_refresh', component_property="n_intervals")
)
def stream_table(value):
    return get_table().to_dict('records')


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
