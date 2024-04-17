__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
# Third party libraries
from dash import dcc, html
import dash_daq as daq
# Custom libraries
from utilities.utilities import load_yaml

# Loading the styles
styles = load_yaml(os.path.join("assets", "styles.yaml"))

# User configuration
update_interval_ms = 2050
update_interval_ms_slow = 5*60*1000

# Objects
device_ping_distribution = html.Div(className="row", children=[
    html.Div(className="six columns", children=[
        html.H3(children="Ping distribution Google (last 24h) [ms]",
                style={'textAlign': 'center',
                       'color': '#FFFFFF'}
                ),
        dcc.Graph(id='device_ping_distribution_graph')
    ]),
    html.Div(className="six columns", children=[
        html.H3(children="Downtime time (last 24h)",
                style={'textAlign': 'center',
                       'color': '#FFFFFF'}
                ),
        html.Div(children=[
            daq.LEDDisplay(
                style={
                    'margin-bottom': 0,  # Or whatever number suits your needs
                    'margin-top': 80
                },
                id="downtime_led",
                value="200",
                size=180,
                color="#FFFFFF",
                backgroundColor="#111111",
                label="seconds",
                labelPosition="bottom",
            )],
            className="text-center"),
    ])
])

infrastructure_figure = html.Div([
    html.H2(children="Infrastructure [ms]",
            style={'textAlign': 'center',
                   'color': '#FFFFFF'}
            ),
    dcc.Graph(id='infrastructure_graph')])

# Tab definition and layout
ping_tab = dcc.Tab(label='Ping',
                   style=styles["tab_style"],
                   selected_style=styles["tab_selected_style"],
                   children=[
                       # Interval for automatic updates
                       dcc.Interval(
                           id='interval_refresh_ping',
                           interval=update_interval_ms,
                           n_intervals=0
                       ),
                       # Interval for automatic updates
                       dcc.Interval(
                           id='interval_refresh_ping_slow',
                           interval=update_interval_ms_slow,
                           n_intervals=0
                       ),
                       # Distribution and downtime
                       device_ping_distribution,
                       # Title and Graph
                       infrastructure_figure,
                   ])
