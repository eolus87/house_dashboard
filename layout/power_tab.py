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
update_interval_ms = 2050

# Initialization
power_tab = dcc.Tab(label='Power',
                    style=styles["tab_style"],
                    selected_style=styles["tab_selected_style"], children=[
                        # Interval for automatic updates
                        dcc.Interval(
                            id='interval_refresh_power',
                            interval=update_interval_ms,
                            n_intervals=0
                        ),

                        # Title and Graph
                        html.H2(children="Power [W]",
                                style={'textAlign': 'center',
                                       'color': '#FFFFFF'}
                                ),
                        dcc.Graph(id='power_graph'),
                      ])
