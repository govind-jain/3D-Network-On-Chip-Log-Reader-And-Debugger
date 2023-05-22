from dash import dcc, html
from dash.dependencies import Input, Output, State
from packet_logger_app import display_seperate as ds


def get_packet_section_layout():
    packet_layout = [html.H2('Packet logger', style={'text-align': 'center', 'padding': '20px', 'font-size': '30px'}),
                     dcc.Input(id='packet-id-input_files', type='text', placeholder='Enter Packet ID', value=''),
                     html.Button('Show Packet Path', id='show-packet-path'),
                     html.Div(id='input-output-container'),
                     html.Div([dcc.Graph(id='display-packets')]),
                     html.Div([html.Div(id='selected-content-packet-logger'), ]),
                     html.Div([
                         dcc.Textarea(id="log-text-packet-logger", value="Please select the above options...",
                                      style={'width': '75%', 'height': 200}, )
                     ])]

    return packet_layout


def inside_update_output(value, node_coordinates, node_limits, packet_details):
    packet_id = int(value)
    co_ordinates_collector = []
    max_buffer_length = -1
    output_buffer_position = -1
    input_buffer_position = -1
    # check if packet_id is in packet_details
    packet_details_new = []
    if packet_id in packet_details.keys():
        for x in packet_details[packet_id]:
            if max_buffer_length < x[4]:
                max_buffer_length = x[4]
        packet_details_new = sorted(packet_details[packet_id], key=lambda x: x[3])
        break_point = None
        for i in range(len(packet_details_new)):
            if packet_details_new[i][3] == 1:
                break_point = i
                break
        packet_details_new = sorted(packet_details_new[:break_point], key=lambda x: x[5],
                                    reverse=True) + packet_details_new[break_point:]
        # sort clock_cycle of packet_details[packet_id] in decreasing order if buffer_id is 0
    idx = 0
    for x in packet_details_new:
        node_id = x[1]
        dir_id = x[2]
        buffer_id = x[3]
        position = x[4]
        clock_cycle = x[5]
        if idx != 0:
            if packet_details_new[idx - 1][1] != node_id:
                output_buffer_position = -1
                input_buffer_position = -1
        coordinates = [node_coordinates[node_id][0], node_coordinates[node_id][1], node_coordinates[node_id][2],
                       buffer_id, clock_cycle, position, node_id]
        if buffer_id:
            output_buffer_position += 1
            position = output_buffer_position
        else:
            input_buffer_position += 1
            position = input_buffer_position
        dif = (position + 1) * node_limits[node_id][dir_id] / (max_buffer_length + 1)
        offset = node_limits[node_id][dir_id] / (max_buffer_length + 1)
        match dir_id:
            case 0:
                coordinates[0] += dif
                if buffer_id:
                    coordinates[2] += offset
                else:
                    coordinates[2] -= offset
            case 1:
                coordinates[0] -= dif
                if buffer_id:
                    coordinates[2] += offset
                else:
                    coordinates[2] -= offset
            case 2:
                coordinates[1] += dif
                if buffer_id:
                    coordinates[0] += offset
                else:
                    coordinates[0] -= offset
            case 3:
                coordinates[1] -= dif
                if buffer_id:
                    coordinates[0] += offset
                else:
                    coordinates[0] -= offset
            case 4:
                coordinates[2] += dif
                if buffer_id:
                    coordinates[1] += offset
                else:
                    coordinates[1] -= offset
            case 5:
                coordinates[2] -= dif
                if buffer_id:
                    coordinates[1] += offset
                else:
                    coordinates[1] -= offset
        co_ordinates_collector.append(coordinates)
        idx += 1
    return packet_id, co_ordinates_collector


def register_packet_path_callbacks(app, switches, connections, node_coordinates, node_limits, packet_details):
    @app.callback(
        [  # Output('input-output-container', 'children'),
            Output('display-packets', 'figure'),
            Output('selected-content-packet-logger', 'children'),
            Output('log-text-packet-logger', 'value'),
        ],
        [Input('show-packet-path', 'n_clicks')],
        [State('packet-id-input_files', 'value')],
        prevent_initial_call=True)
    def update_output(n_click, value):
        if n_click is not None:
            packet_id, co_ordinates_collector = inside_update_output(value, node_coordinates, node_limits,
                                                                     packet_details)
            print(packet_details)
            fig = ds.packet_show(switches, co_ordinates_collector, connections)
            selected = f'log files for packet_id {packet_id} are :'
            relevant = ''
            if packet_id in packet_details.keys():
                for x in packet_details[packet_id]:
                    relevant += f'clock cycle = {x[5]} layer_id = {x[0]} node_id = {x[1]} direction_id = {x[2]} buffer_id = {x[3]} position = {x[4]}\n'
            if relevant == '':
                relevant = 'no log files for this packet'
            return fig, selected, relevant

    return app
