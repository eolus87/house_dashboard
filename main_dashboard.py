__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
# Third party libraries
import pandas as pd
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
# Custom libraries
from utilities.utilities import load_yaml
from labourers.leader import Leader
from network.ping_function import ping_function
from network.pingdataextractor import PingDataExtractor
from network.devicetype import DeviceType
from power.power_function import power_function
from control.control_functions import switch_on_function, switch_off_function

# Configuration
configuration_path = os.path.join("config", "config.yaml")
pd.options.plotting.backend = "plotly"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
configuration = load_yaml(configuration_path)
styles = load_yaml(os.path.join("assets", "styles.yaml"))

# Initialization network
ping_leader = Leader(configuration["network"], ping_function)
ping_leader.start()
ping_data_extractor = PingDataExtractor(configuration["network"], ping_leader)
init_table = ping_data_extractor.retrieve_ping_stats(DeviceType.PERSONAL_DEVICE, 10)

# Initialization energy
power_leader = Leader(configuration["energy"], power_function)
power_leader.start()

# Dash layout
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(style={'backgroundColor': '#111111'},
                      children=[
                          html.H1(children="Home Server",
                                  style={'textAlign': 'center',
                                         'color': '#FFFFFF'}),
                          dcc.Tabs([
                              dcc.Tab(label='Network',
                                      style=styles["tab_style"],
                                      selected_style=styles["tab_selected_style"], children=[
                                          html.H2(children="Infrastructure ping [ms]",
                                                  style={'textAlign': 'center',
                                                         'color': '#FFFFFF'}
                                                  ),
                                          dcc.Interval(
                                              id='interval_refresh_network',
                                              interval=1 * 2050,  # in milliseconds
                                              n_intervals=0
                                          ),
                                          dcc.Graph(id='infrastructure_graph'),

                                          # Title and personal devices figure
                                          html.H2(children="Personal devices ping [ms]",
                                                  style={'textAlign': 'center',
                                                         'color': '#FFFFFF'}
                                                  ),
                                          html.Div(
                                              dash_table.DataTable(data=init_table.to_dict('records'),
                                                                   columns=[{"name": i, "id": i} for i in
                                                                            init_table.columns],
                                                                   style_cell={'textAlign': 'center',
                                                                               'backgroundColor': '#111111',
                                                                               'color': 'white',
                                                                               'font_size': '20px'},
                                                                   style_header={'border': '1px solid black',
                                                                                 'font_size': '30px'},
                                                                   style_as_list_view=True,
                                                                   id='tbl')
                                          ),
                                        ]),
                              dcc.Tab(label='Energy',
                                      style=styles["tab_style"],
                                      selected_style=styles["tab_selected_style"], children=[
                                          html.H2(children="Energy [W]",
                                                  style={'textAlign': 'center',
                                                         'color': '#FFFFFF'}
                                                  ),
                                          dcc.Interval(
                                              id='interval_refresh_energy',
                                              interval=1 * 2050,  # in milliseconds
                                              n_intervals=0
                                          ),
                                          dcc.Graph(id='energy_graph'),
                                        ]),
                              dcc.Tab(label='Temperature',
                                      style=styles["tab_style"],
                                      selected_style=styles["tab_selected_style"],
                                      children=[]),

                              dcc.Tab(label='Control',
                                      style=styles["tab_style"],
                                      selected_style=styles["tab_selected_style"], children=[
                                          # Button
                                          html.Button('Printer',
                                                      id='button-example-1'),
                                          html.Div(id='output-container-button',
                                                   children='Enter a value and press submit',
                                                   style={'color': '#FFFFFF'}
                                                   )
                                      ]),


                          ])

                      ])


# Callbacks
@app.callback(
    Output(component_id='infrastructure_graph', component_property='figure'),
    Input(component_id='interval_refresh_network', component_property="n_intervals")
)
def stream_fig_network(value):
    df = ping_data_extractor.retrieve_ping_data(DeviceType.INFRASTRUCTURE)
    fig = df.plot(template='plotly_dark')
    fig.update_layout(
        xaxis_title="Samples [-]",
        yaxis_title="Ping [ms]",
    )
    return fig


@app.callback(
    Output(component_id='tbl', component_property='data'),
    Input(component_id='interval_refresh_network', component_property="n_intervals")
)
def stream_table(value):
    return ping_data_extractor.retrieve_ping_stats(DeviceType.PERSONAL_DEVICE, 10).to_dict('records')


@app.callback(
    Output(component_id='energy_graph', component_property='figure'),
    Input(component_id='interval_refresh_energy', component_property="n_intervals")
)
def stream_fig_energy(value):
    df = power_leader.target_deque
    fig = df.plot(template='plotly_dark')
    fig.update_layout(
        xaxis_title="Samples [-]",
        yaxis_title="Energy [W]",
    )
    return fig


@app.callback(
    Output(component_id='output-container-button', component_property='children'),
    [Input(component_id='button-example-1', component_property='n_clicks')],
    )
def update_output(n_clicks):
    if n_clicks is not None:
        if n_clicks % 2 == 0:
            switch_off_function("192.168.0.49")
        else:
            switch_on_function("192.168.0.49")

    return 'The button has been clicked {} times'.format(
        n_clicks
    )


app.run_server(host="0.0.0.0", port=8069, dev_tools_ui=True,  # debug=True,
               dev_tools_hot_reload=True, threaded=True)
