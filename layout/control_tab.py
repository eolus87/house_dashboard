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
power_tab = dcc.Tab(label='Control',
                    style=styles["tab_style"],
                    selected_style=styles["tab_selected_style"], children=[
                        # Button
                        # html.Button('Printer',
                        #             id='button-example-1'),
                        # html.Div(id='output-container-button',
                        #          children='Enter a value and press submit',
                        #          style={'color': '#FFFFFF'}
                        #          )
                      ])
