import plotly.graph_objs as go


def fill_coordinates(x_switches, y_switches, z_switches, x_repeaters, y_repeaters, z_repeaters):

    node_coordinates = []
    number_of_switches = len(x_switches)
    number_of_repeaters = len(x_repeaters)

    for itr in range(0, number_of_switches):
        node_coordinates.append([x_switches[itr], y_switches[itr], z_switches[itr]])

    for itr in range(0, number_of_repeaters):
        node_coordinates.append([x_repeaters[itr], y_repeaters[itr], z_repeaters[itr]])

    return node_coordinates


def network_topology_display(switches, connections):
    # we need to separate the X,Y,Z coordinates for Plotly
    x_switches = []  # x-coordinates of switches
    y_switches = []  # y-coordinates of switches
    z_switches = []  # z-coordinates of switches

    x_repeaters = []  # x-coordinates of repeaters
    y_repeaters = []  # y-coordinates of repeaters
    z_repeaters = []  # z-coordinates of repeaters

    # we need to create lists that contain the starting and ending coordinates of each connection
    x_direct_connections = []  # x-coordinates of src and dest switches for direct connections
    y_direct_connections = []  # y-coordinates of src and dest switches for direct connections
    z_direct_connections = []  # z-coordinates of src and dest switches for direct connections

    x_indirect_connections = []  # x-coordinates of src and dest nodes for indirect connections
    y_indirect_connections = []  # y-coordinates of src and dest nodes for indirect connections
    z_indirect_connections = []  # z-coordinates of src and dest nodes for indirect connections

    colors_for_indirect_connections = ['green', 'blue']
    variety_of_indirect_connections = len(colors_for_indirect_connections)

    for sz in range(variety_of_indirect_connections):
        x_indirect_connections.append([])
        y_indirect_connections.append([])
        z_indirect_connections.append([])

    # create lists to store the labels of switches and repeaters
    switch_labels = []
    repeater_labels = []

    for switch_data in switches:
        x_switches.append(switch_data[0])
        y_switches.append(switch_data[1])
        z_switches.append(switch_data[2])
        switch_labels.append(f'Switch ID = {switch_data[3]}')

    repeater_counter = len(switches)

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

                    repeater_labels.append(f'Repeater ID = {repeater_counter}')
                    repeater_counter = repeater_counter + 1

                # Create connection b/w curr_node and prev_node
                x_coords_start_end_of_indirect_connection = [x_prev_node, x_curr_node, None]
                x_indirect_connections[itr % variety_of_indirect_connections] += x_coords_start_end_of_indirect_connection

                y_coords_start_end_of_indirect_connection = [y_prev_node, y_curr_node, None]
                y_indirect_connections[itr % variety_of_indirect_connections] += y_coords_start_end_of_indirect_connection

                z_coords_start_end_of_indirect_connection = [z_prev_node, z_curr_node, None]
                z_indirect_connections[itr % variety_of_indirect_connections] += z_coords_start_end_of_indirect_connection

                x_prev_node = x_curr_node
                y_prev_node = y_curr_node
                z_prev_node = z_curr_node

        else:
            x_coords_start_end_of_direct_connection = [x_src_switch, x_dest_switch, None]
            x_direct_connections += x_coords_start_end_of_direct_connection

            y_coords_start_end_of_direct_connection = [y_src_switch, y_dest_switch, None]
            y_direct_connections += y_coords_start_end_of_direct_connection

            z_coords_start_end_of_direct_connection = [z_src_switch, z_dest_switch, None]
            z_direct_connections += z_coords_start_end_of_direct_connection

    # Include the traces we want to plot and create a figure
    data = []

    # Create a trace for the switches
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

    # create a trace for the repeaters
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

    # create a trace for the direct_connections
    trace_direct_connections = go.Scatter3d(
        x=x_direct_connections,
        y=y_direct_connections,
        z=z_direct_connections,
        mode='lines',
        line=dict(color='black', width=3),
        hoverinfo='none')

    data.append(trace_direct_connections)

    # create a trace for the indirect_connections
    for itr in range(variety_of_indirect_connections):

        trace_indirect_connections = go.Scatter3d(
            x=x_indirect_connections[itr],
            y=y_indirect_connections[itr],
            z=z_indirect_connections[itr],
            mode='lines',
            line=dict(color=colors_for_indirect_connections[itr], width=3),
            hoverinfo='none')

        data.append(trace_indirect_connections)

    # Define layout for the 3D plot
    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='X-axis'),
            yaxis=dict(title='Y-axis'),
            zaxis=dict(title='Z-axis')
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    fig = go.Figure(data=data, layout=layout)

    # We also want the coordinates of switches and repeater in one array
    node_coordinates = fill_coordinates(x_switches, y_switches, z_switches, x_repeaters, y_repeaters, z_repeaters)

    return fig, node_coordinates
