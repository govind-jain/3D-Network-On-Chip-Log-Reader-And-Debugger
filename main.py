import dash
from topology_display_app.topology_reader import *
from topology_display_app.network_topology_display import *
from topology_display_app.layout_and_callbacks import *
from switch_logger_app.switch_log_reader import *
from switch_logger_app.buffer_contents_display import *
from switch_logger_app.layout_and_callbacks import *
from packet_logger_app.packet_log_reader import *
from packet_logger_app.packet_path_display import *
from packet_logger_app.layout_and_callbacks import *

number_of_topology_layers = 5

# Need to identify using logger
switches, connections = read_topology_config('input_files/topology.txt')
topology_display_fig = network_topology_display(switches, connections)
switch_array = [f"{'Switch'} {i}" for i in range(len(switches))]
layer_array = [f"{'Layer'} {i}" for i in range(number_of_topology_layers)]

max_clock_cycle = 100

app = dash.Dash(__name__)
register_buffer_contents_callbacks(app)
register_packet_path_callbacks(app)


def get_app_layout():
    topology_layout = get_topology_display_layout(topology_display_fig)
    switch_layout = get_switch_section_layout(layer_array, switch_array, max_clock_cycle)
    packet_layout = get_packet_section_layout()

    layout_array = []

    layout_array.extend(topology_layout)
    layout_array.append(html.Hr())
    layout_array.extend(switch_layout)
    layout_array.append(html.Hr())
    layout_array.extend(packet_layout)

    return html.Div(layout_array)


if __name__ == '__main__':
    app.layout = get_app_layout()
    app.run_server(debug=True)
