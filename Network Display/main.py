import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from network_topology_display import *
from input_reader import *

# Need to identify using logger
max_clock_cycle = 100
switches, connections = read_graph_data('./../input/topology.txt')
fig = network_topology_display(switches, connections)
switch_array = ['Switch 0', 'Switch 1', 'Switch 2', 'Switch 3']
layer_array = ['Layer 0', 'Layer 1', 'Layer 2', 'Layer 3']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2('Network Topology', style={'text-align': 'center', 'font-size': '30px'}),
    dcc.Graph(id='network-graph', figure=fig, style={'padding-bottom': '5%'}),
    html.Hr(),
    html.H2('Switch logger', style={'text-align': 'center', 'padding': '20px', 'font-size': '30px'}),
    html.Div([
        html.Div([
            html.Label("Select Layer:"),
            dcc.Dropdown(
                id='layer-selector',
                options=layer_array
            )
        ], style={'width': '12%', 'display': 'inline-block', 'padding': '0 20px'}),
        html.Div([
            html.Label("Select Node:"),
            dcc.Dropdown(
                id='switch-selector',
                options=switch_array
            )
        ], style={'width': '12%', 'display': 'inline-block', 'padding': '0 20px'}),
        html.Div([
            html.Label("Select Clock Cycle:"),
            dcc.Slider(
                id='clock-cycle-selector',
                min=0,
                max=max_clock_cycle,
                value=0,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '0 20px'}),
        html.Div([
            html.Button("Go", id="show-buffer-contents")
        ], style={'width': '10%', 'display': 'inline-block', 'padding': '0 20px'}),
    ], style={'margin': '40px'}),
    html.Div(id='buffer-contents', style={'display': 'none'}),
    # dcc.Input(id='packet-id-input', type='number', placeholder='Enter Packet ID'),
    # html.Button('Show Packet Path', id='show-packet-path'),
    # dcc.Graph(id='packet-path-graph')
])


# @app.callback(
#     Output('buffer-contents', 'children'),
#     [Input('network-graph', 'clickData'),
#      Input('clock-cycle-slider', 'value')])
# def display_buffer_contents(clickData, clock_cycle):
#     if clickData is None:
#         return None
#     node_id = clickData['points'][0]['text']
#     return clickData


#     buffer_contents = get_buffer_contents(node_id, clock_cycle)
#     return create_buffer_contents_plot(buffer_contents)


# @app.callback(
#     Output('packet-path-graph', 'figure'),
#     [Input('show-packet-path', 'n_clicks')],
#     [dash.dependencies.State('packet-id-input', 'value')])
# def display_packet_path(n_clicks, packet_id):
#     if n_clicks is None or packet_id is None:
#         return go.Figure()
#     packet_path = get_packet_path(packet_id)
#     return create_packet_path_plot(nodes, packet_path)


if __name__ == '__main__':
    app.run_server(debug=True)
