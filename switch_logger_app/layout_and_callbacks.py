from types import NoneType
from dash import dcc, html
from dash.dependencies import Input, Output, State
from switch_logger_app.buffer_contents_display import buffer_contents_display

# Write all the callbacks for this app inside the function
def register_buffer_contents_callbacks(app, node_log):
    @app.callback(
        [Output('display-buffer-content', 'figure'),
         Output('selected-content', 'children'),
         Output('log-text', 'value'),
        ],
        [Input('go-button', 'n_clicks')],
        [
         State('clock-cycle-selector', 'value'),
         State('layer-selector', 'value'),
         State('switch-selector', 'value')
        ],
        prevent_initial_call=True
        )
    def display_buffer_contents(n_clicks, clock_cycle, layer_id, switch_id):
        relevant_logs = ""
        # print(node_log)
        for log in node_log:
            if clock_cycle == int(log['clock_cycle']) and layer_id == log['layer_id'] and switch_id == log['node_id']:
                relevant_logs += "CLOCK_CYLCE={} LAYER_ID={} NODE_ID={} DIR_ID={} BUFFER_TYPE={} POS={} PACKET_ID={}\n".format(log["clock_cycle"],log["layer_id"],log["node_id"],log["dir_id"],log["buffer_type"],log['position_idx'],log['packet_id'])

        if len(relevant_logs) == 0:
            relevant_logs = "No relevant logs are there for the selected options."

        if layer_id is NoneType or switch_id is NoneType:
            relevant_logs = "Layer Id or Switch Id is not selected."

        selected = f'Relevant log files for the selected CLOCK_CYCLE: {clock_cycle}, LAYER_ID: {layer_id}, SWITCH_ID: {switch_id}'    

        fig = buffer_contents_display(node_log, clock_cycle, layer_id, switch_id)

        if n_clicks is not None:
            return fig, selected, relevant_logs


def get_switch_section_layout(layer_array, switch_array, max_clock_cycle):
    switch_section_layout = [
        html.H2('Switch logger', style={'text-align': 'center', 'padding': '20px', 'font-size': '30px'}),
        html.Div([
            html.Div([
                html.Label('Select Layer: '),
                dcc.Dropdown(
                    id='layer-selector',
                    options=layer_array,
                    placeholder="Layer ID"
                ),
            ], style={'width': '200px', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '35px'}),  
            html.Div([
                html.Label('Select Switch: '),
                dcc.Dropdown(
                    id='switch-selector',
                    options=switch_array,
                    placeholder="Switch ID"
                ),
            ], style={'width': '200px', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '35px'}),
            html.Div([
                html.Label('Select the Clock Cycle: '),
                dcc.Input(
                    id='clock-cycle-selector',
                    type='number',
                    placeholder="Clock Cycle",
                    min=0,
                    max=max_clock_cycle,
                    value=0,
                ),
            ], style={'width': '200px', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '35px'}),
            html.Button("Go", id="go-button"),
            html.Div([
                dcc.Graph(id='display-buffer-content'),
            ]),
            html.Div([
                html.Div(id='selected-content'),
            ]),
            html.Div([
                dcc.Textarea(id="log-text", value="Please select the above options...", style={'width': '75%', 'height': 200},)
            ]),
        ], style={'margin': '40px'}),
    ]

    return switch_section_layout
