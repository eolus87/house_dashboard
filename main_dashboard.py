__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
# Third party libraries
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import psycopg2
# Custom libraries
from utilities.utilities import load_yaml
from datahandling.dataextractor import DataExtractor
from ping.pingdevicetype import PingDeviceType
from power.powerdevicetype import PowerDeviceType
from layout.ping_tab import ping_tab
from layout.power_tab import power_tab

# User configuration
configuration_path = os.path.join("config", "config.yaml")

# Style
pd.options.plotting.backend = "plotly"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Configuration
configuration = load_yaml(configuration_path)
hours_to_display = configuration["hours_to_display"]
hours_for_tables = configuration["hours_for_tables"]

# Database connection
db_config = configuration["postgresql"]
conn = psycopg2.connect(
    host=db_config["ip"],
    port=db_config["port"],
    user=db_config["user"],
    password=db_config["password"])

# Initialization ping
ping_data_extractor = DataExtractor(configuration, "ping", conn)

# Initialization energy
power_data_extractor = DataExtractor(configuration, "power", conn)

# Dash layout
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(style={'backgroundColor': '#111111'},
                      children=[
                          html.H1(children="House Dashboard",
                                  style={'textAlign': 'center',
                                         'color': '#FFFFFF'}),
                          dcc.Tabs([
                              ping_tab,
                              power_tab
                          ])
                      ])


# Callbacks
@app.callback(
    Output(component_id='infrastructure_graph', component_property='figure'),
    Input(component_id='interval_refresh_ping', component_property="n_intervals")
)
def stream_fig_network(value):
    # Retrieve data
    dfs_dict = ping_data_extractor.retrieve_data(
        PingDeviceType.INFRASTRUCTURE,
        hours_to_display)
    fig = go.Figure()
    # Plot
    for df_index, df_name in enumerate(dfs_dict):
        fig.add_trace(go.Scatter(x=dfs_dict[df_name].index, y=dfs_dict[df_name]["value"],
                                 name=df_name))
    fig.update_layout(
        xaxis_title="Date and Time",
        yaxis_title="Ping [ms]",
        template="plotly_dark"
    )
    return fig


@app.callback(
    Output(component_id='personal_devices_table', component_property='data'),
    Input(component_id='interval_refresh_ping', component_property="n_intervals")
)
def stream_table(value):
    return ping_data_extractor.retrieve_stats(
        PingDeviceType.PERSONAL_DEVICE,
        hours_for_tables).to_dict('records')


@app.callback(
    Output(component_id='power_graph', component_property='figure'),
    Input(component_id='interval_refresh_power', component_property="n_intervals")
)
def stream_fig_power(value):
    # Retrieve data
    dfs_dict = power_data_extractor.retrieve_data(
        PowerDeviceType.PLUG,
        hours_to_display)
    fig = go.Figure()
    # Plot
    for df_index, df_name in enumerate(dfs_dict):
        fig.add_trace(go.Scatter(x=dfs_dict[df_name].index, y=dfs_dict[df_name]["value"],
                                 name=df_name))
    fig.update_layout(
        xaxis_title="Date and Time",
        yaxis_title="Power [W]",
        template="plotly_dark"
    )
    return fig


# @app.callback(
#     Output(component_id='output-container-button', component_property='children'),
#     [Input(component_id='button-example-1', component_property='n_clicks')],
#     )
# def update_output(n_clicks):
#     if n_clicks is not None:
#         if n_clicks % 2 == 0:
#             switch_off_function("192.168.0.49")
#         else:
#             switch_on_function("192.168.0.49")
#
#     return 'The button has been clicked {} times'.format(
#         n_clicks
#     )

try:
    app.run_server(host="0.0.0.0", port=8069, dev_tools_ui=True,  # debug=True,
                   dev_tools_hot_reload=True, threaded=True)

except KeyboardInterrupt as keyinterrupt:
    print(f"Exiting gracefully")
    conn.close()

except Exception as inst:
    print(f"Exception registered: {inst}")
    conn.close()
