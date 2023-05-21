import plotly.graph_objs as go


def packet_show(switches, co_ordinates, connections):
    last_node_id = len(switches) - 1
    x_switches = []  # x-coordinates of switches
    y_switches = []  # y-coordinates of switches
    z_switches = []  # z-coordinates of switches

    x_repeaters = []  # x-coordinates of repeaters
    y_repeaters = []  # y-coordinates of repeaters
    z_repeaters = []  # z-coordinates of repeaters

    x_snapshot_output_buffer = []
    y_snapshot_output_buffer = []
    z_snapshot_output_buffer = []

    x_snapshot_input_buffer = []
    y_snapshot_input_buffer = []
    z_snapshot_input_buffer = []

    x_direct_connections = []  # x-coordinates of src and dest switches for direct connections
    y_direct_connections = []  # y-coordinates of src and dest switches for direct connections
    z_direct_connections = []  # z-coordinates of src and dest switches for direct connections

    switch_labels = []
    snapshot_output_labels = []
    snapshot_input_labels = []
    repeater_labels = []

    for snap_data in co_ordinates:
        if (snap_data[3] == 1):
            x_snapshot_output_buffer.append(snap_data[0])
            y_snapshot_output_buffer.append(snap_data[1])
            z_snapshot_output_buffer.append(snap_data[2])
            identifier = None
            if snap_data[6] > last_node_id:
                identifier = 'R'
            else:
                identifier = snap_data[6]
            snapshot_output_labels.append(f'clock cycle = {snap_data[4]} position = {snap_data[5]} at {identifier}')
        else:
            x_snapshot_input_buffer.append(snap_data[0])
            y_snapshot_input_buffer.append(snap_data[1])
            z_snapshot_input_buffer.append(snap_data[2])
            identifier = None
            if snap_data[6] > last_node_id:
                identifier = 'R'
            else:
                identifier = snap_data[6]
            snapshot_input_labels.append(f'clock cycle = {snap_data[4]} position = {snap_data[5]} at {identifier}')

    for switch_data in switches:
        x_switches.append(switch_data[0])
        y_switches.append(switch_data[1])
        z_switches.append(switch_data[2])
        switch_labels.append(f'Switch ID = {switch_data[3]}')

    for connection_data in connections:

        src_switch_id = connection_data[0]
        dest_switch_id = connection_data[1]
        number_of_repeaters = connection_data[2]

        x_src_switch = x_switches[src_switch_id]
        y_src_switch = y_switches[src_switch_id]
        z_src_switch = z_switches[src_switch_id]

        x_dest_switch = x_switches[dest_switch_id]
        y_dest_switch = y_switches[dest_switch_id]
        z_dest_switch = z_switches[dest_switch_id]

        if number_of_repeaters != 0:

            x_diff_adder = (x_dest_switch - x_src_switch) / (number_of_repeaters + 1)
            y_diff_adder = (y_dest_switch - y_src_switch) / (number_of_repeaters + 1)
            z_diff_adder = (z_dest_switch - z_src_switch) / (number_of_repeaters + 1)

            x_prev_node = x_src_switch
            y_prev_node = y_src_switch
            z_prev_node = z_src_switch

            for itr in range(1, number_of_repeaters + 2):

                # Compute coordinates of curr node using prev node
                x_curr_node = x_prev_node + x_diff_adder
                y_curr_node = y_prev_node + y_diff_adder
                z_curr_node = z_prev_node + z_diff_adder

                # Store the repeater details for displaying
                if itr <= number_of_repeaters:
                    x_repeaters.append(x_curr_node)
                    y_repeaters.append(y_curr_node)
                    z_repeaters.append(z_curr_node)

                    repeater_labels.append(f'Repeater ID = {src_switch_id}_{dest_switch_id}_{itr}')

                x_prev_node = x_curr_node
                y_prev_node = y_curr_node
                z_prev_node = z_curr_node

        x_coords_start_end_of_direct_connection = [x_src_switch, x_dest_switch, None]
        x_direct_connections += x_coords_start_end_of_direct_connection

        y_coords_start_end_of_direct_connection = [y_src_switch, y_dest_switch, None]
        y_direct_connections += y_coords_start_end_of_direct_connection

        z_coords_start_end_of_direct_connection = [z_src_switch, z_dest_switch, None]
        z_direct_connections += z_coords_start_end_of_direct_connection

    data = []

    # create a trace for the switches
    trace_switches = go.Scatter3d(
        x=x_switches,
        y=y_switches,
        z=z_switches,
        mode='markers',
        text=switch_labels,
        marker=dict(symbol='circle',
                    size=16,
                    color='red')
    )

    data.append(trace_switches)

    trace_repeaters = go.Scatter3d(
        x=x_repeaters,
        y=y_repeaters,
        z=z_repeaters,
        mode='markers',
        text=repeater_labels,
        marker=dict(symbol='circle',
                    size=10,
                    color='black')
    )

    data.append(trace_repeaters)

    trace_snapshot_output_buffer = go.Scatter3d(
        x=x_snapshot_output_buffer,
        y=y_snapshot_output_buffer,
        z=z_snapshot_output_buffer,
        mode='markers',
        text=snapshot_output_labels,
        marker=dict(symbol='circle',
                    size=3,
                    color='green')
    )

    data.append(trace_snapshot_output_buffer)

    trace_snapshot_input_buffer = go.Scatter3d(
        x=x_snapshot_input_buffer,
        y=y_snapshot_input_buffer,
        z=z_snapshot_input_buffer,
        mode='markers',
        text=snapshot_input_labels,
        marker=dict(symbol='circle',
                    size=3,
                    color='blue')
    )

    data.append(trace_snapshot_input_buffer)

    trace_direct_connections = go.Scatter3d(
        x=x_direct_connections,
        y=y_direct_connections,
        z=z_direct_connections,
        mode='lines',
        line=dict(color='black', width=3),
        hoverinfo='none')

    data.append(trace_direct_connections)

    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='X-axis'),
            yaxis=dict(title='Y-axis'),
            zaxis=dict(title='Z-axis')
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    fig = go.Figure(data=data, layout=layout)
    return fig
