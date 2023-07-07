__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
# Third party libraries
from dash import dcc, html
# Custom libraries
from utilities.utilities import load_yaml

# Loading the styles
styles = load_yaml(os.path.join("assets", "styles.yaml"))

# User configuration
update_interval_ms = 30050

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

                                # Title and Graph
                                html.H2(children="Temperature [C]",
                                        style={'textAlign': 'center',
                                               'color': '#FFFFFF'}
                                        ),
                                dcc.Graph(id='temperature_graph'),
                            ])
