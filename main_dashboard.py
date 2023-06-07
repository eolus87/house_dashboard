__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
# Third party libraries
import pandas as pd
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
# Custom libraries
from ping_classes.pingmanager import PingManager
from ping_classes.pingdataextractor import PingDataExtractor
from ping_classes.devicetype import DeviceType

# Configuration
configuration_path = os.path.join("config", "config.yaml")
pd.options.plotting.backend = "plotly"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialization
ping_manager = PingManager(configuration_path)
ping_manager.start()
ping_data_extractor = PingDataExtractor(configuration_path, ping_manager)
init_table = ping_data_extractor.retrieve_ping_stats(DeviceType.PERSONAL_DEVICE, 10)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# Dash layout
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(style={'backgroundColor': '#111111'},
                      children=[
                          html.H1(children="Home Server",
                                  style={'textAlign': 'center',
                                         'color': '#FFFFFF'}),
                          dcc.Tabs([
                              dcc.Tab(label='Network', style=tab_style, selected_style=tab_selected_style, children=[
                                  html.H2(children="Infrastructure ping [ms]",
                                          style={'textAlign': 'center',
                                                 'color': '#FFFFFF'}
                                          ),
                                  dcc.Interval(
                                      id='interval_refresh',
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
                                                           columns=[{"name": i, "id": i} for i in init_table.columns],
                                                           style_cell={'textAlign': 'center',
                                                                       'backgroundColor': '#111111',
                                                                       'color': 'white',
                                                                       'font_size': '20px'},
                                                           style_header={'border': '1px solid black',
                                                                         'font_size': '30px'},
                                                           style_as_list_view=True,
                                                           id='tbl')
                                  ),

                                  # Button
                                  html.Button('Submit',
                                              id='button-example-1'),
                                  html.Div(id='output-container-button',
                                           children='Enter a value and press submit',
                                           style={'color': '#FFFFFF'}
                                           )
                              ]),
                              dcc.Tab(label='Energy', style=tab_style, selected_style=tab_selected_style, children=[])
                          ])


                      ])


# Callbacks
@app.callback(
    Output(component_id='infrastructure_graph', component_property='figure'),
    Input(component_id='interval_refresh', component_property="n_intervals")
)
def stream_fig(value):
    df = ping_data_extractor.retrieve_ping_data(DeviceType.INFRASTRUCTURE)
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
    return ping_data_extractor.retrieve_ping_stats(DeviceType.PERSONAL_DEVICE, 10).to_dict('records')


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
