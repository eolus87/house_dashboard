__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
# Third party libraries
from dash import dcc, html
import plotly.graph_objects as go
# Custom libraries
from utilities.utilities import load_yaml

# Loading the styles
styles = load_yaml(os.path.join("assets", "styles.yaml"))

# User configuration
update_interval_ms = 10 * 1000
update_interval_ms_slow = 300 * 1000 + 50

# Objects
current_temp = html.Div(className="row", children=[
    html.Div(className="six columns", children=[
        dcc.Graph(id='dining_room_indicator')
    ]),
    html.Div(className="six columns", children=[
            dcc.Graph(id='bed_room_indicator')
        ])
])

week_temperature = html.Div([
    html.H2(children="Temperature [C]",
            style={'textAlign': 'center',
                   'color': '#FFFFFF'}
            ),
    dcc.Graph(id='temperature_graph')])


# Initialization
temperature_tab = dcc.Tab(label='Temperature',
                          style=styles["tab_style"],
                          selected_style=styles["tab_selected_style"], children=[
                                # Interval for automatic updates
                                dcc.Interval(
                                    id='interval_refresh_temperature',
                                    interval=update_interval_ms,
                                    n_intervals=0
                                ),
                                dcc.Interval(
                                    id='interval_refresh_temperature_slow',
                                    interval=update_interval_ms_slow,
                                    n_intervals=0
                                ),
                                # Title and Graph
                                current_temp,
                                week_temperature
                            ])
