import dash
from input_files.input_reader import *
from topology_display_app.network_topology_display import *
from topology_display_app.layout_and_callbacks import *
from switch_logger_app.layout_and_callbacks import *
from packet_logger_app.layout_and_callbacks import *

# Need to identify using logger
switches, connections = read_topology_config('input_files/topology.txt')
topology_display_fig = network_topology_display(switches, connections)
switch_array = ['Switch 0', 'Switch 1', 'Switch 2', 'Switch 3']
layer_array = ['Layer 0', 'Layer 1', 'Layer 2', 'Layer 3']

max_clock_cycle = 100

app = dash.Dash(__name__)
register_buffer_contents_callbacks(app)
register_packet_path_callbacks(app)


def get_app_layout():
    topology_layout = get_topology_display_layout(topology_display_fig)

    switch_layout = get_switch_section_layout(layer_array, switch_array, max_clock_cycle)

    # packet_layout = [dcc.Input(id='packet-id-input_files', type='number', placeholder='Enter Packet ID'),
    #                  html.Button('Show Packet Path', id='show-packet-path'),
    #                  dcc.Graph(id='packet-path-graph')]

    layout_array = []

    layout_array.extend(topology_layout)
    layout_array.append(html.Hr())
    layout_array.extend(switch_layout)
    # layout_array.append(html.Hr())
    # layout_array.extend(packet_layout)

    layout = html.Div(layout_array)

    return layout


if __name__ == '__main__':
    app.layout = get_app_layout()
    app.run_server(debug=True)
