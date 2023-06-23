__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
# Third party libraries
from dash import dcc, html, dash_table
import pandas as pd
# Custom libraries
from utilities.utilities import load_yaml

# Loading the styles
styles = load_yaml(os.path.join("assets", "styles.yaml"))

# User configuration
update_interval_ms = 2050

# Initialization
init_table = pd.DataFrame(columns=["Device", "Mean", "Std", "Available"])

ping_tab = dcc.Tab(label='Ping',
                   style=styles["tab_style"],
                   selected_style=styles["tab_selected_style"], children=[
                        # Interval for automatic updates
                        dcc.Interval(
                            id='interval_refresh_ping',
                            interval=update_interval_ms,
                            n_intervals=0
                        ),

                        # Title and Graph
                        html.H2(children="Infrastructure [ms]",
                                style={'textAlign': 'center',
                                       'color': '#FFFFFF'}
                                ),
                        dcc.Graph(id='infrastructure_graph'),

                        # Title and Table
                        html.H2(children="Personal devices [ms]",
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
                                                 id='personal_devices_table')
                        ),
                   ])
