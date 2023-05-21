from dash import dcc, html
from dash.dependencies import Input, Output, State
from packet_logger_app import packet_log_reader as plr
from packet_logger_app import display_seperate as ds


def get_packet_section_layout():
    packet_layout = [dcc.Input(id='packet-id-input_files', type='text', placeholder='Enter Packet ID', value=''),
                     html.Button('Show Packet Path', id='show-packet-path'),
                     html.Div(id='input-output-container'),
                     html.Div([dcc.Graph(id='display-packets')]),
                     html.Div([html.Div(id='selected-content'), ]),
                     html.Div([
                         dcc.Textarea(id="log-text", value="Please select the above options...",
                                      style={'width': '75%', 'height': 200}, )
                     ])]

    return packet_layout


def register_packet_path_callbacks(app, switches, connections, node_coordinates, node_limits):
    @app.callback(
        [  # Output('input-output-container', 'children'),
            Output('display-packets', 'figure'),
            Output('selected-content', 'children'),
            Output('log-text', 'value'),
        ],
        [Input('show-packet-path', 'n_clicks')],
        [State('packet-id-input_files', 'value')],
        prevent_initial_call=True)
    def update_output(n_click, value):
        if n_click is not None:
            packet_id = int(value)
            packet_details = plr.read_packet_log('input_files/packet_logger.txt')
            co_ordinates_collector = []
            coordinates = []
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

                '''for switch_data in switches:
                    if node_id == switch_data[3]:
                        coordinates = [switch_data[0],switch_data[1],switch_data[2],buffer_id,clock_cycle]'''
                coordinates = [node_coordinates[node_id][0], node_coordinates[node_id][1], node_coordinates[node_id][2],
                               buffer_id, clock_cycle, position, node_id]

                '''coordinate_of_nodes_around = []
                for y in connections:
                    if y[0] == node_id:
                        for switch_data in switches:
                            if y[1] == switch_data[3]:
                                temp_list = [switch_data[0],switch_data[1],switch_data[2],y[2]]
                                coordinate_of_nodes_around.append(temp_list)
                # for given dir_id find opposite node_id and its coordinate and edge length
                opposite_node = []
                numbers_of_repeater = 0

                if dir_id == 0 or dir_id == 1:
                    for child in coordinate_of_nodes_around:
                        if child[1] == coordinates[1] and child[2] == coordinates[2]:
                            opposite_node = [child[0],child[1],child[2]]
                            numbers_of_repeater = child[3]
                elif dir_id == 2 or dir_id == 3:
                    for child in coordinate_of_nodes_around:
                        if child[0] == coordinates[0] and child[2] == coordinates[2]:
                            opposite_node = [child[0],child[1],child[2]]
                            numbers_of_repeater = child[3]
                elif dir_id == 4 or dir_id == 5:
                    for child in coordinate_of_nodes_around:
                        if child[1] == coordinates[1] and child[0] == coordinates[0]:
                            opposite_node = [child[0],child[1],child[2]]
                            numbers_of_repeater = child[3]'''

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
