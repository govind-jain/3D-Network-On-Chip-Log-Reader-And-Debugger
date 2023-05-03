import plotly.graph_objs as go
import numpy as np


def buffer_contents_display(node_log, clock_cycle, layer_id, switch_id):

    # Contains strings of format position_idx, dir_id, packet_id
    input_buf = []
    output_buf = []

    # Fetching only the relevant logs based on query
    # Storing based on type of buffer
    for log in node_log:
        if int(log['clock_cycle']) == int(clock_cycle) and int(log['layer_id']) == int(layer_id) \
                and int(switch_id) == int(log['node_id']):

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
    packet_initial_position = 0.1
    packet_spacing = 0.3

    # data stores the objects that needs to be displayed
    data = []

    # We set the coordinates to 0,0,0 of the switch that we are looking for
    x_switch = [0]
    y_switch = [0]
    z_switch = [0]

    switch_label = []
    switch_label.append(f'Switch ID = {switch_id}')

    trace_switch = go.Scatter3d(
        x=x_switch,
        y=y_switch,
        z=z_switch,
        mode='markers',
        text=switch_label,
        marker=dict(symbol='circle',
                    size=node_radius,
                    color=node_color)
    )

    data.append(trace_switch)

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
        for packet_id in input_buf_x:
            input_buf_x_labels.append(f'Packet ID = {packet_id}')

        trace_input_buf_x = go.Scatter3d(
            x=np.linspace(packet_initial_position, packet_spacing, num=len(input_buf_x)),
            y=[0.002] * len(input_buf_x),
            z=[0] * len(input_buf_x),
            mode='markers',
            text=input_buf_x_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_x)

    if len(input_buf_x_neg) != 0:
        input_buf_x_neg_labels = []
        for packet_id in input_buf_x_neg:
            input_buf_x_neg_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_x_neg = go.Scatter3d(
            x=np.linspace(-1*packet_initial_position, -1*packet_spacing, num=len(input_buf_x_neg)),
            y=[0.002] * len(input_buf_x_neg),
            z=[0] * len(input_buf_x_neg),
            mode='markers',
            text=input_buf_x_neg_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_x_neg)

    if len(input_buf_y) != 0:
        input_buf_y_labels = []
        for packet_id in input_buf_y:
            input_buf_y_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_y = go.Scatter3d(
            x=[0.002] * len(input_buf_y),
            y=np.linspace(packet_initial_position, packet_spacing, num=len(input_buf_y)),
            z=[0] * len(input_buf_y),
            mode='markers',
            text=input_buf_y_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_y)

    if len(input_buf_y_neg) != 0:
        input_buf_y_neg_labels = []
        for packet_id in input_buf_y_neg:
            input_buf_y_neg_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_y_neg = go.Scatter3d(
            x=[0.002] * len(input_buf_y_neg),
            y=np.linspace(-1*packet_initial_position, -1*packet_spacing, num=len(input_buf_y_neg)),
            z=[0] * len(input_buf_y_neg),
            mode='markers',
            text=input_buf_y_neg_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_y_neg)

    if len(input_buf_z) != 0:
        input_buf_z_labels = []
        for packet_id in input_buf_z:
            input_buf_z_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_z = go.Scatter3d(
            x=[0.002] * len(input_buf_z),
            y=[0] * len(input_buf_z),
            z=np.linspace(packet_initial_position, packet_spacing, num=len(input_buf_z)),
            mode='markers',
            text=input_buf_z_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=input_buf_packet_color)
        )
        data.append(trace_input_buf_z)

    if len(input_buf_z_neg) != 0:
        input_buf_z_neg_labels = []
        for packet_id in input_buf_z_neg:
            input_buf_z_neg_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_z_neg = go.Scatter3d(
            x=[0.002] * len(input_buf_z_neg),
            y=[0] * len(input_buf_z_neg),
            z=np.linspace(-1*packet_initial_position, -1*packet_spacing, num=len(input_buf_z_neg)),
            mode='markers',
            text=input_buf_z_neg_labels,
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
        for packet_id in output_buf_x:
            output_buf_x_labels.append(f'Packet ID = {packet_id}')
        output_buf_x_labels.reverse()
        trace_output_buf_x = go.Scatter3d(
            x=np.linspace(packet_initial_position, packet_spacing, num=len(output_buf_x)),
            y=[-0.002] * len(output_buf_x),
            z=[0] * len(output_buf_x),
            mode='markers',
            text=output_buf_x_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_x)

    if len(output_buf_x_neg) != 0:
        output_buf_x_neg_labels = []
        for packet_id in output_buf_x_neg:
            output_buf_x_neg_labels.append(f'Packet ID = {packet_id}')
        output_buf_x_neg_labels.reverse()
        trace_output_buf_x_neg = go.Scatter3d(
            x=np.linspace(-1*packet_initial_position, -1*packet_spacing, num=len(output_buf_x_neg)),
            y=[-0.002] * len(output_buf_x_neg),
            z=[0] * len(output_buf_x_neg),
            mode='markers',
            text=output_buf_x_neg_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_x_neg)

    if len(output_buf_y) != 0:
        output_buf_y_labels = []
        for packet_id in output_buf_y:
            output_buf_y_labels.append(f'Packet ID = {packet_id}')
        output_buf_y_labels.reverse()
        trace_output_buf_y = go.Scatter3d(
            x=[-0.002] * len(output_buf_y),
            y=np.linspace(packet_initial_position, packet_spacing, num=len(output_buf_y)),
            z=[0] * len(output_buf_y),
            mode='markers',
            text=output_buf_y_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_y)

    if len(output_buf_y_neg) != 0:
        output_buf_y_neg_labels = []
        for packet_id in output_buf_y_neg:
            output_buf_y_neg_labels.append(f'Packet ID = {packet_id}')
        output_buf_y_neg_labels.reverse()
        trace_output_buf_y_neg = go.Scatter3d(
            x=[-0.002] * len(output_buf_y_neg),
            y=np.linspace(-1*packet_initial_position, -1*packet_spacing, num=len(output_buf_y_neg)),
            z=[0] * len(output_buf_y_neg),
            mode='markers',
            text=output_buf_y_neg_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_y_neg)

    if len(output_buf_z) != 0:
        output_buf_z_labels = []
        for packet_id in output_buf_z:
            output_buf_z_labels.append(f'Packet ID = {packet_id}')
        output_buf_z_labels.reverse()
        trace_output_buf_z = go.Scatter3d(
            x=[-0.002] * len(output_buf_z),
            y=[0] * len(output_buf_z),
            z=np.linspace(packet_initial_position, packet_spacing, num=len(output_buf_z)),
            mode='markers',
            text=output_buf_z_labels,
            marker=dict(symbol='circle',
                        size=packet_radius,
                        color=output_buf_packet_color)
        )
        data.append(trace_output_buf_z)

    if len(output_buf_z_neg) != 0:
        output_buf_z_neg_labels = []
        for packet_id in output_buf_z_neg:
            output_buf_z_neg_labels.append(f'Packet ID = {packet_id}')
        output_buf_z_neg_labels.reverse()
        trace_output_buf_z_neg = go.Scatter3d(
            x=[-0.002] * len(output_buf_z_neg),
            y=[0] * len(output_buf_z_neg),
            z=np.linspace(-1*packet_initial_position, -1*packet_spacing, num=len(output_buf_z_neg)),
            mode='markers',
            text=output_buf_z_neg_labels,
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
    return fig
