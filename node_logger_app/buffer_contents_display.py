import plotly.graph_objs as go
import numpy as np


def buffer_contents_display(node_log, clock_cycle, layer_id, node_id):
    # Contains strings of format position_idx, dir_id, packet_id
    input_buf = []
    output_buf = []

    # Fetching only the relevant logs based on query
    # Storing based on type of buffer
    for log in node_log:
        if int(log['clock_cycle']) == int(clock_cycle) and int(log['layer_id']) == int(layer_id) \
                and int(node_id) == int(log['node_id']):

            if int(log['buffer_type']) == 0:
                input_buf.append("{} {} {}".format(log['position_idx'], log['dir_id'], log['packet_id']))
            elif int(log['buffer_type']) == 1:
                output_buf.append("{} {} {}".format(log['position_idx'], log['dir_id'], log['packet_id']))

    input_buf.sort(key=lambda x: int(x.split()[0]))
    output_buf.sort(key=lambda x: int(x.split()[0]))

    # Data constants used to display
    node_radius = 16
    packet_radius = 8
    node_color = 'red'
    input_buf_packet_color = 'blue'
    output_buf_packet_color = 'green'
    packet_initial_position = 0.015
    packet_spacing_axis = 0.015
    packet_spacing_separate = 0.005

    # data stores the objects that needs to be displayed
    data = []

    # We set the coordinates to 0,0,0 of the node that we are looking for
    x_node = [0]
    y_node = [0]
    z_node = [0]

    node_label = []
    node_label.append(f'Node ID = {node_id}')

    trace_node = go.Scatter3d(
        x=x_node,
        y=y_node,
        z=z_node,
        mode='markers',
        text=node_label,
        hovertemplate='%{text}<extra></extra>',
        marker=dict(symbol='circle',
                    size=node_radius,
                    color=node_color)
    )

    data.append(trace_node)

    ############################################################
    ###################### INPUT BUFFERS #######################
    ############################################################

    input_buf_x = []
    input_buf_x_neg = []
    input_buf_y = []
    input_buf_y_neg = []
    input_buf_z = []
    input_buf_z_neg = []

    for element in input_buf:
        if int(element.split(' ')[1]) == 0:
            input_buf_x.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 1:
            input_buf_x_neg.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 2:
            input_buf_y.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 3:
            input_buf_y_neg.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 4:
            input_buf_z.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 5:
            input_buf_z_neg.append(int(element.split(' ')[2]))

    ######## DEBUGGING ######## 
    # print(input_buf)
    # print(input_buf_x)
    # print(input_buf_x_neg)
    # print(input_buf_y)
    # print(input_buf_y_neg)
    # print(input_buf_z)
    # print(input_buf_z_neg)

    # Display buffer contents

    if len(input_buf_x) != 0:
        input_buf_x_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(input_buf_x)-1)*packet_spacing_axis

        for packet_id in input_buf_x:
            input_buf_x_labels.append(f'Packet ID = {packet_id} | DIR = E | Type = IP | Pos = {counter}')
            counter = counter + 1

        trace_input_buf_x = go.Scatter3d(
            x=np.linspace(packet_initial_position, packet_final_position, num=len(input_buf_x)),
            y=[packet_spacing_separate] * len(input_buf_x),
            z=[0] * len(input_buf_x),
            mode='markers',
            text=input_buf_x_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_x)

    if len(input_buf_x_neg) != 0:
        input_buf_x_neg_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(input_buf_x_neg) - 1) * packet_spacing_axis

        for packet_id in input_buf_x_neg:
            input_buf_x_neg_labels.append(f'Packet ID = {packet_id} | DIR = W | Type = IP | Pos = {counter}')
            counter = counter + 1

        trace_input_buf_x_neg = go.Scatter3d(
            x=np.linspace(-1 * packet_initial_position, -1 * packet_final_position, num=len(input_buf_x_neg)),
            y=[packet_spacing_separate] * len(input_buf_x_neg),
            z=[0] * len(input_buf_x_neg),
            mode='markers',
            text=input_buf_x_neg_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_x_neg)

    if len(input_buf_y) != 0:
        input_buf_y_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(input_buf_y) - 1) * packet_spacing_axis

        for packet_id in input_buf_y:
            input_buf_y_labels.append(f'Packet ID = {packet_id} | DIR = N | Type = IP | Pos = {counter}')
            counter = counter + 1

        trace_input_buf_y = go.Scatter3d(
            x=[packet_spacing_separate] * len(input_buf_y),
            y=np.linspace(packet_initial_position, packet_final_position, num=len(input_buf_y)),
            z=[0] * len(input_buf_y),
            mode='markers',
            text=input_buf_y_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_y)

    if len(input_buf_y_neg) != 0:
        input_buf_y_neg_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(input_buf_y_neg) - 1) * packet_spacing_axis

        for packet_id in input_buf_y_neg:
            input_buf_y_neg_labels.append(f'Packet ID = {packet_id} | DIR = S | Type = IP | Pos = {counter}')
            counter = counter + 1

        trace_input_buf_y_neg = go.Scatter3d(
            x=[packet_spacing_separate] * len(input_buf_y_neg),
            y=np.linspace(-1 * packet_initial_position, -1 * packet_final_position, num=len(input_buf_y_neg)),
            z=[0] * len(input_buf_y_neg),
            mode='markers',
            text=input_buf_y_neg_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_y_neg)

    if len(input_buf_z) != 0:
        input_buf_z_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(input_buf_z) - 1) * packet_spacing_axis

        for packet_id in input_buf_z:
            input_buf_z_labels.append(f'Packet ID = {packet_id} | DIR = T | Type = IP | Pos = {counter}')
            counter = counter + 1

        trace_input_buf_z = go.Scatter3d(
            x=[packet_spacing_separate] * len(input_buf_z),
            y=[0] * len(input_buf_z),
            z=np.linspace(packet_initial_position, packet_final_position, num=len(input_buf_z)),
            mode='markers',
            text=input_buf_z_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_z)

    if len(input_buf_z_neg) != 0:
        input_buf_z_neg_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(input_buf_z_neg) - 1) * packet_spacing_axis

        for packet_id in input_buf_z_neg:
            input_buf_z_neg_labels.append(f'Packet ID = {packet_id} | DIR = D | Type = IP | Pos = {counter}')
            counter = counter + 1

        trace_input_buf_z_neg = go.Scatter3d(
            x=[packet_spacing_separate] * len(input_buf_z_neg),
            y=[0] * len(input_buf_z_neg),
            z=np.linspace(-1 * packet_initial_position, -1 * packet_final_position, num=len(input_buf_z_neg)),
            mode='markers',
            text=input_buf_z_neg_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_z_neg)

    ############################################################
    ###################### OUTPUT BUFFERS ######################
    ############################################################

    output_buf_x = []
    output_buf_x_neg = []
    output_buf_y = []
    output_buf_y_neg = []
    output_buf_z = []
    output_buf_z_neg = []

    for element in output_buf:
        if int(element.split(' ')[1]) == 0:
            output_buf_x.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 1:
            output_buf_x_neg.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 2:
            output_buf_y.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 3:
            output_buf_y_neg.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 4:
            output_buf_z.append(int(element.split(' ')[2]))
        elif int(element.split(' ')[1]) == 5:
            output_buf_z_neg.append(int(element.split(' ')[2]))

    if len(output_buf_x) != 0:
        output_buf_x_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(output_buf_x) - 1) * packet_spacing_axis

        for packet_id in output_buf_x:
            output_buf_x_labels.append(f'Packet ID = {packet_id} | DIR = E | Type = OP | Pos = {counter}')
            counter = counter + 1

        output_buf_x_labels.reverse()

        trace_output_buf_x = go.Scatter3d(
            x=np.linspace(packet_initial_position, packet_final_position, num=len(output_buf_x)),
            y=[-1 * packet_spacing_separate] * len(output_buf_x),
            z=[0] * len(output_buf_x),
            mode='markers',
            text=output_buf_x_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_x)

    if len(output_buf_x_neg) != 0:
        output_buf_x_neg_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(output_buf_x_neg) - 1) * packet_spacing_axis

        for packet_id in output_buf_x_neg:
            output_buf_x_neg_labels.append(f'Packet ID = {packet_id} | DIR = W | Type = OP | Pos = {counter}')
            counter = counter + 1

        output_buf_x_neg_labels.reverse()

        trace_output_buf_x_neg = go.Scatter3d(
            x=np.linspace(-1 * packet_initial_position, -1 * packet_final_position, num=len(output_buf_x_neg)),
            y=[-1 * packet_spacing_separate] * len(output_buf_x_neg),
            z=[0] * len(output_buf_x_neg),
            mode='markers',
            text=output_buf_x_neg_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_x_neg)

    if len(output_buf_y) != 0:
        output_buf_y_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(output_buf_y) - 1) * packet_spacing_axis

        for packet_id in output_buf_y:
            output_buf_y_labels.append(f'Packet ID = {packet_id} | DIR = N | Type = OP | Pos = {counter}')
            counter = counter + 1

        output_buf_y_labels.reverse()

        trace_output_buf_y = go.Scatter3d(
            x=[-1 * packet_spacing_separate] * len(output_buf_y),
            y=np.linspace(packet_initial_position, packet_final_position, num=len(output_buf_y)),
            z=[0] * len(output_buf_y),
            mode='markers',
            text=output_buf_y_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_y)

    if len(output_buf_y_neg) != 0:
        output_buf_y_neg_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(output_buf_y_neg) - 1) * packet_spacing_axis

        for packet_id in output_buf_y_neg:
            output_buf_y_neg_labels.append(f'Packet ID = {packet_id} | DIR = S | Type = OP | Pos = {counter}')
            counter = counter + 1

        output_buf_y_neg_labels.reverse()

        trace_output_buf_y_neg = go.Scatter3d(
            x=[-1 * packet_spacing_separate] * len(output_buf_y_neg),
            y=np.linspace(-1 * packet_initial_position, -1 * packet_final_position, num=len(output_buf_y_neg)),
            z=[0] * len(output_buf_y_neg),
            mode='markers',
            text=output_buf_y_neg_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_y_neg)

    if len(output_buf_z) != 0:
        output_buf_z_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(output_buf_z) - 1) * packet_spacing_axis

        for packet_id in output_buf_z:
            output_buf_z_labels.append(f'Packet ID = {packet_id} | DIR = T | Type = OP | Pos = {counter}')
            counter = counter + 1

        output_buf_z_labels.reverse()

        trace_output_buf_z = go.Scatter3d(
            x=[-1 * packet_spacing_separate] * len(output_buf_z),
            y=[0] * len(output_buf_z),
            z=np.linspace(packet_initial_position, packet_final_position, num=len(output_buf_z)),
            mode='markers',
            text=output_buf_z_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_z)

    if len(output_buf_z_neg) != 0:
        output_buf_z_neg_labels = []
        counter = 0
        packet_final_position = packet_initial_position + (len(output_buf_z_neg) - 1) * packet_spacing_axis

        for packet_id in output_buf_z_neg:
            output_buf_z_neg_labels.append(f'Packet ID = {packet_id} | DIR = B | Type = OP | Pos = {counter}')
            counter = counter + 1

        output_buf_z_neg_labels.reverse()

        trace_output_buf_z_neg = go.Scatter3d(
            x=[-1 * packet_spacing_separate] * len(output_buf_z_neg),
            y=[0] * len(output_buf_z_neg),
            z=np.linspace(-1 * packet_initial_position, -1 * packet_final_position, num=len(output_buf_z_neg)),
            mode='markers',
            text=output_buf_z_neg_labels,
            hovertemplate='%{text}<extra></extra>',
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_z_neg)

    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='X-axis', showspikes=True, visible=True),
            yaxis=dict(title='Y-axis', showspikes=True, visible=True),
            zaxis=dict(title='Z-axis', showspikes=True, visible=True)
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    fig = go.Figure(data=data, layout=layout)

    # Add 3D axes at the origin
    pos_x_limit = max(len(input_buf_x), len(output_buf_x)) * packet_spacing_axis
    neg_x_limit = -1 * max(len(input_buf_x_neg), len(output_buf_x_neg)) * packet_spacing_axis
    pos_y_limit = max(len(input_buf_y), len(output_buf_y)) * packet_spacing_axis
    neg_y_limit = -1 * max(len(input_buf_y_neg), len(output_buf_y_neg)) * packet_spacing_axis
    pos_z_limit = max(len(input_buf_z), len(output_buf_z)) * packet_spacing_axis
    neg_z_limit = -1 * max(len(input_buf_z_neg), len(output_buf_z_neg)) * packet_spacing_axis

    fig.add_trace(
        go.Scatter3d(x=[0, pos_x_limit], y=[0, 0], z=[0, 0], mode='lines', name='X', line=dict(color='black')))
    fig.add_trace(
        go.Scatter3d(x=[0, neg_x_limit], y=[0, 0], z=[0, 0], mode='lines', name='-X', line=dict(color='black')))
    fig.add_trace(
        go.Scatter3d(x=[0, 0], y=[0, pos_y_limit], z=[0, 0], mode='lines', name='Y', line=dict(color='black')))
    fig.add_trace(
        go.Scatter3d(x=[0, 0], y=[0, neg_y_limit], z=[0, 0], mode='lines', name='-Y', line=dict(color='black')))
    fig.add_trace(
        go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, pos_z_limit], mode='lines', name='Z', line=dict(color='black')))
    fig.add_trace(
        go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, neg_z_limit], mode='lines', name='-Z', line=dict(color='black')))

    return fig
