import dash
from topology_display_app.topology_reader import *
from topology_display_app.network_topology_display import *
from topology_display_app.layout_and_callbacks import *
from topology_display_app.topology_processing import *
from node_logger_app.node_log_reader import *
from node_logger_app.layout_and_callbacks import *
from packet_logger_app.layout_and_callbacks import *
from packet_logger_app.packet_log_reader import *

# Read topology configuration file and generate required data
switches, connections = read_topology_config('input_files/topology.txt')
node_coordinates, node_limits = topology_processing(switches, connections)
topology_display_fig = network_topology_display(switches, connections)

# Read node logger file and generate required data
node_logs, max_clock_cycle, layer_array, node_array = read_node_log('input_files/node_logger.txt')
packet_logs = read_packet_log('input_files/packet_logger.txt')

app = dash.Dash(__name__)
register_buffer_contents_callbacks(app, node_logs)
register_packet_path_callbacks(app, topology_display_fig, len(switches), node_coordinates, node_limits, packet_logs)


def get_app_layout():
    topology_section_layout = get_topology_display_layout(topology_display_fig)
    node_section_layout = get_node_section_layout(layer_array, node_array, max_clock_cycle, len(switches))
    packet_section_layout = get_packet_section_layout()

    layout_array = []

    layout_array.extend(topology_section_layout)
    layout_array.append(html.Hr())
    layout_array.extend(node_section_layout)
    layout_array.append(html.Hr())
    layout_array.extend(packet_section_layout)

    return html.Div(layout_array)


if __name__ == '__main__':
    app.layout = get_app_layout()
    app.run_server(debug=True)
