import plotly.graph_objs as go
import numpy as np

def buffer_contents_display(node_log, clock_cycle, layer_id, switch_id):
    # We set the coordinates to 0,0,0 of the switch that we are looking for
    x_switch = [0]  
    y_switch = [0]  
    z_switch = [0]  

    switch_label = []
    switch_label.append(f'Switch ID = {switch_id}')    

    input_buf = [] # position_idx, dir_id, packet_id
    output_buf = []

    ############################################################
    ###################### INPUT BUFFERS #######################
    ############################################################
    
    for log in node_log:
        if int(switch_id) == int(log['node_id']) and int(log['buffer_type']) == 0 and int(log['clock_cycle']) == int(clock_cycle) and int(log['layer_id']) == int(layer_id):
            input_buf.append("{} {} {}".format(log['position_idx'], log['dir_id'], log['packet_id']))

    input_buf.sort(key=lambda x: int(x.split()[0]))

    input_buf_x = []
    input_buf_x_neg = []
    input_buf_y = []
    input_buf_y_neg = []
    input_buf_z = []
    input_buf_z_neg = []

    for str in input_buf:
        if int(str.split(' ')[1]) == 0:
            input_buf_x.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 1:
            input_buf_x_neg.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 2:
            input_buf_y.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 3:
            input_buf_y_neg.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 4:
            input_buf_z.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 5:
            input_buf_z_neg.append(int(str.split(' ')[2]))
            
    data = []

    trace_switch = go.Scatter3d(
        x=x_switch,
        y=y_switch,
        z=z_switch,
        mode='markers',
        text=switch_label,
        marker=dict(symbol='circle',
                    size=16,
                    color='red')
    )

    data.append(trace_switch)

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
            x=np.linspace(0.2,1, num=len(input_buf_x)),
            y=[0.002]*len(input_buf_x),
            z=[0]*len(input_buf_x),
            mode='markers',
            text=input_buf_x_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='blue')
        )
        data.append(trace_input_buf_x)

    
    if len(input_buf_x_neg) != 0:
        input_buf_x_neg_labels = []
        for packet_id in input_buf_x_neg:
            input_buf_x_neg_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_x_neg = go.Scatter3d(
            x=np.linspace(0.2, -1, num=len(input_buf_x_neg)),
            y=[0.002]*len(input_buf_x_neg),
            z=[0]*len(input_buf_x_neg),
            mode='markers',
            text=input_buf_x_neg_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='blue')
        )
        data.append(trace_input_buf_x_neg)

    if len(input_buf_y) != 0:
        input_buf_y_labels = []
        for packet_id in input_buf_y:
            input_buf_y_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_y = go.Scatter3d(
            x=[0.002]*len(input_buf_y),
            y=np.linspace(0.2, 1, num=len(input_buf_y)),
            z=[0]*len(input_buf_y),
            mode='markers',
            text=input_buf_y_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='blue')
        )
        data.append(trace_input_buf_y)

    if len(input_buf_y_neg) != 0:
        input_buf_y_neg_labels = []
        for packet_id in input_buf_y_neg:
            input_buf_y_neg_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_y_neg = go.Scatter3d(
            x=[0.002]*len(input_buf_y_neg),
            y=np.linspace(0.2, -1, num=len(input_buf_y_neg)),
            z=[0]*len(input_buf_y_neg),
            mode='markers',
            text=input_buf_y_neg_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='blue')
        )
        data.append(trace_input_buf_y_neg)

    if len(input_buf_z) != 0:
        input_buf_z_labels = []
        for packet_id in input_buf_z:
            input_buf_z_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_z = go.Scatter3d(
            x=[0.002]*len(input_buf_z),
            y=[0]*len(input_buf_z),
            z=np.linspace(0.2, 1, num=len(input_buf_z)),
            mode='markers',
            text=input_buf_z_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='blue')
        )
        data.append(trace_input_buf_z)
    
    if len(input_buf_z_neg) != 0:
        input_buf_z_neg_labels = []
        for packet_id in input_buf_z_neg:
            input_buf_z_neg_labels.append(f'Packet ID = {packet_id}')
        trace_input_buf_z_neg = go.Scatter3d(
            x=[0.002]*len(input_buf_z_neg),
            y=[0]*len(input_buf_z_neg),
            z=np.linspace(0.2, -1, num=len(input_buf_z_neg)),
            mode='markers',
            text=input_buf_z_neg_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='blue')
        )
        data.append(trace_input_buf_z_neg)

    ############################################################
    ###################### OUTPUT BUFFERS ######################
    ############################################################

    for log in node_log:
        if int(switch_id) == int(log['node_id']) and int(log['buffer_type']) == 1 and int(clock_cycle) == int(log['clock_cycle']) and int(layer_id) == int(log['layer_id']):
            output_buf.append("{} {} {}".format(log['position_idx'], log['dir_id'], log['packet_id']))

    output_buf.sort(key=lambda x: int(x.split()[0]))

    output_buf_x = []
    output_buf_x_neg = []
    output_buf_y = []
    output_buf_y_neg = []
    output_buf_z = []
    output_buf_z_neg = []

    for str in output_buf:
        if int(str.split(' ')[1]) == 0:
            output_buf_x.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 1:
            output_buf_x_neg.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 2:
            output_buf_y.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 3:
            output_buf_y_neg.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 4:
            output_buf_z.append(int(str.split(' ')[2]))
        elif int(str.split(' ')[1]) == 5:
            output_buf_z_neg.append(int(str.split(' ')[2]))
    
    if len(output_buf_x) != 0:
        output_buf_x_labels = []
        for packet_id in output_buf_x:
            output_buf_x_labels.append(f'Packet ID = {packet_id}')
        output_buf_x_labels.reverse()
        trace_output_buf_x = go.Scatter3d(
            x=np.linspace(0.2,1, num=len(output_buf_x)),
            y=[-0.002]*len(output_buf_x),
            z=[0]*len(output_buf_x),
            mode='markers',
            text=output_buf_x_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='green')
        )
        data.append(trace_output_buf_x)

    if len(output_buf_x_neg) != 0:
        output_buf_x_neg_labels = []
        for packet_id in output_buf_x_neg:
            output_buf_x_neg_labels.append(f'Packet ID = {packet_id}')
        output_buf_x_neg_labels.reverse()
        trace_output_buf_x_neg = go.Scatter3d(
            x=np.linspace(0.2,-1, num=len(output_buf_x_neg)),
            y=[-0.002]*len(output_buf_x_neg),
            z=[0]*len(output_buf_x_neg),
            mode='markers',
            text=output_buf_x_neg_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='green')
        )
        data.append(trace_output_buf_x_neg)

    if len(output_buf_y) != 0:
        output_buf_y_labels = []
        for packet_id in output_buf_y:
            output_buf_y_labels.append(f'Packet ID = {packet_id}')
        output_buf_y_labels.reverse()
        trace_output_buf_y = go.Scatter3d(
            x=[-0.002]*len(output_buf_y),
            y=np.linspace(0.2,1, num=len(output_buf_y)),
            z=[0]*len(output_buf_y),
            mode='markers',
            text=output_buf_y_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='green')
        )
        data.append(trace_output_buf_y)

    if len(output_buf_y_neg) != 0:
        output_buf_y_neg_labels = []
        for packet_id in output_buf_y_neg:
            output_buf_y_neg_labels.append(f'Packet ID = {packet_id}')
        output_buf_y_neg_labels.reverse()
        trace_output_buf_y_neg = go.Scatter3d(
            x=[-0.002]*len(output_buf_y_neg),
            y=np.linspace(0.2,-1, num=len(output_buf_y_neg)),
            z=[0]*len(output_buf_y_neg),
            mode='markers',
            text=output_buf_y_neg_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='green')
        )
        data.append(trace_output_buf_y_neg)

    if len(output_buf_z) != 0:
        output_buf_z_labels = []
        for packet_id in output_buf_z:
            output_buf_z_labels.append(f'Packet ID = {packet_id}')
        output_buf_z_labels.reverse()
        trace_output_buf_z = go.Scatter3d(
            x=[-0.002]*len(output_buf_z),
            y=[0]*len(output_buf_z),
            z=np.linspace(0.2,1, num=len(output_buf_z)),
            mode='markers',
            text=output_buf_z_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='green')
        )
        data.append(trace_output_buf_z)

    if len(output_buf_z_neg) != 0:
        output_buf_z_neg_labels = []
        for packet_id in output_buf_z_neg:
            output_buf_z_neg_labels.append(f'Packet ID = {packet_id}')
        output_buf_z_neg_labels.reverse()
        trace_output_buf_z_neg = go.Scatter3d(
            x=[-0.002]*len(output_buf_z_neg),
            y=[0]*len(output_buf_z_neg),
            z=np.linspace(0.2,-1, num=len(output_buf_z_neg)),
            mode='markers',
            text=output_buf_z_neg_labels,
            marker=dict(symbol='circle',
                        size=8,
                        color='green')
        )
        data.append(trace_output_buf_z_neg)

    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='X-axis',showspikes=True,visible=True),
            yaxis=dict(title='Y-axis',showspikes=True,visible=True),
            zaxis=dict(title='Z-axis',showspikes=True,visible=True)
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    fig = go.Figure(data=data, layout=layout)
    return fig
