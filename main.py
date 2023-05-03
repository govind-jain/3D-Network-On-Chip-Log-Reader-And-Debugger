import dash
from topology_display_app.topology_reader import *
from topology_display_app.network_topology_display import *
from topology_display_app.layout_and_callbacks import *
from topology_display_app.topology_processing import *
from switch_logger_app.switch_log_reader import *
from switch_logger_app.buffer_contents_display import *
from switch_logger_app.layout_and_callbacks import *
from packet_logger_app.packet_log_reader import *
from packet_logger_app.packet_path_display import *
from packet_logger_app.layout_and_callbacks import *

# Read topology configuration file and generate required data
switches, connections = read_topology_config('input_files/topology.txt')
node_coordinates, node_limits = topology_processing(switches, connections)
topology_display_fig = network_topology_display(switches, connections)

# Read switch logger file and generate required data
node_log, max_clock_cycle, layer_array, switch_array = read_switch_config('input_files/switch_logger.txt')

app = dash.Dash(__name__)
register_buffer_contents_callbacks(app, node_log)
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
