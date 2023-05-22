from dash import dcc, html
from dash.dependencies import Input, Output, State
from packet_logger_app import packet_path_display as ds


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


def get_packet_log(packet_id, node_coordinates, node_limits, packet_logs):
    packet_log = []
    max_buffer_length = -1
    output_buffer_position = -1
    input_buffer_position = -1

    # check if packet_id is in packet_logs
    packet_details_new = []
    if packet_id in packet_logs.keys():
        for x in packet_logs[packet_id]:
            if max_buffer_length < x[4]:
                max_buffer_length = x[4]

        packet_details_new = sorted(packet_logs[packet_id], key=lambda x: x[3])
        break_point = None

        for i in range(len(packet_details_new)):
            if packet_details_new[i][3] == 1:
                break_point = i
                break

        # sort clock_cycle of packet_details[packet_id] in decreasing order if buffer_id is 0
        packet_details_new = sorted(packet_details_new[:break_point], key=lambda x: x[5],
                                    reverse=True) + packet_details_new[break_point:]

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

        log = [node_coordinates[node_id][0], node_coordinates[node_id][1], node_coordinates[node_id][2],
               buffer_id, clock_cycle, position, node_id, dir_id]

        if buffer_id:
            output_buffer_position += 1
            position = output_buffer_position
        else:
            input_buffer_position += 1
            position = input_buffer_position

        offset = node_limits[node_id][dir_id] / (max_buffer_length + 1)
        dif = (position + 1) * offset

        match dir_id:
            case 0:
                log[0] += dif
                if buffer_id:
                    log[2] += offset
                else:
                    log[2] -= offset
            case 1:
                log[0] -= dif
                if buffer_id:
                    log[2] += offset
                else:
                    log[2] -= offset
            case 2:
                log[1] += dif
                if buffer_id:
                    log[0] += offset
                else:
                    log[0] -= offset
            case 3:
                log[1] -= dif
                if buffer_id:
                    log[0] += offset
                else:
                    log[0] -= offset
            case 4:
                log[2] += dif
                if buffer_id:
                    log[1] += offset
                else:
                    log[1] -= offset
            case 5:
                log[2] -= dif
                if buffer_id:
                    log[1] += offset
                else:
                    log[1] -= offset

        packet_log.append(log)
        idx += 1

    return packet_log


def register_packet_path_callbacks(app, topology_display_fig, number_of_switches, node_coordinates, node_limits,
                                   packet_logs):
    @app.callback(
        [  # Output('input-output-container', 'children'),
            Output('display-packets', 'figure'),
            Output('selected-content-packet-logger', 'children'),
            Output('log-text-packet-logger', 'value'),
        ],
        [Input('show-packet-path', 'n_clicks')],
        [State('packet-id-input_files', 'value')],
        prevent_initial_call=True)
    def update_output(n_click, packet_id):
        if n_click is not None:
            packet_id = int(packet_id)
            packet_log = get_packet_log(packet_id, node_coordinates,
                                        node_limits, packet_logs)
            packet_path_display_fig = ds.packet_path_display(topology_display_fig, number_of_switches,
                                                             packet_log)
            selected = f'Log entries for packet_id {packet_id} are:'
            relevant_logs = ''

            if len(packet_log) != 0:
                for x in packet_logs[packet_id]:
                    relevant_logs += f'CLOCK_CYCLE = {x[5]} LAYER_ID = {x[0]} NODE_ID = {x[1]} DIR_ID = {x[2]} BUFFER_TYPE = {x[3]} POS_IDX = {x[4]}\n'
            else:
                relevant_logs = 'No log entries present for this packet.'

            return packet_path_display_fig, selected, relevant_logs

    return app
