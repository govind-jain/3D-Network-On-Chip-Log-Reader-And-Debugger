from dash import dcc, html
from dash.dependencies import Input, Output, State
from node_logger_app.buffer_contents_display import buffer_contents_display


# Write all the callbacks for this app inside the function
def register_buffer_contents_callbacks(app, node_log):
    @app.callback(
        [Output('display-buffer-content', 'figure'),
         Output('selected-content-node-logger', 'children'),
         Output('log-text-node-logger', 'value'),
         ],
        [Input('go-button', 'n_clicks')
         ],
        [State('clock-cycle-selector', 'value'),
         State('layer-selector', 'value'),
         State('node-selector', 'value')
         ],
        prevent_initial_call=True
    )
    def display_buffer_contents(n_clicks, clock_cycle, layer_id, node_id):
        relevant_logs = ""

        # Get the ID from "Node {ID}"
        node_id = int(node_id.split(' ')[1])

        for log in node_log:
            same_layer = (int(layer_id) == int(log['layer_id']))
            same_clock_cycle = (clock_cycle == int(log['clock_cycle']))
            same_node_id = (node_id == int(log['node_id']))
            # print(same_layer, same_clock_cycle, same_node_id)

            if same_layer and same_clock_cycle and same_node_id:
                relevant_logs += "CLOCK_CYCLE={} LAYER_ID={} NODE_ID={} DIR_ID={} BUFFER_TYPE={} POS={} PACKET_ID={}\n".format(
                    log["clock_cycle"], log["layer_id"], log["node_id"], log["dir_id"], log["buffer_type"],
                    log['position_idx'], log['packet_id'])

        if len(relevant_logs) == 0:
            relevant_logs = "No relevant logs are there for the selected options."

        options_selected = True

        if layer_id is None or node_id is None:
            relevant_logs = "Layer Id or Node Id is not selected."
            options_selected = False

        selected = f'Relevant log files for the selected CLOCK_CYCLE: {clock_cycle}, LAYER_ID: {layer_id}, NODE_ID: {node_id}'

        fig = buffer_contents_display(node_log, clock_cycle, layer_id, node_id)

        if n_clicks is not None:
            if options_selected is True:
                return fig, selected, relevant_logs
            else:
                return None, selected, relevant_logs


def get_node_section_layout(layer_array, node_array, max_clock_cycle, number_of_switches):
    modified_node_list = []

    for node in node_array:
        if int(node) < number_of_switches:
            modified_node_list.append("Switch {}".format(node))
        else:
            modified_node_list.append("Repeater {}".format(node))

    node_section_layout = [
        html.H2('Node logger', style={'text-align': 'center', 'padding': '20px', 'font-size': '30px'}),
        html.Div(id='output-data'),
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
                html.Label('Select Node: '),
                dcc.Dropdown(
                    id='node-selector',
                    options=modified_node_list,
                    placeholder="Node ID"
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
                html.Div(id='selected-content-node-logger', style={'padding-top': '20px'}),
            ]),
            html.Div([
                dcc.Textarea(id="log-text-node-logger", value="Please select the above options...",
                             style={'width': '75%', 'height': 200}, )
            ]),
        ], style={'margin': '40px'}),
    ]

    return node_section_layout
