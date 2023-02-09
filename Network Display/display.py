import plotly.graph_objects as go


def is_sorted_low_to_high(switch_data_1, switch_data_2):

    if switch_data_1[0] != switch_data_2[0]:
        return switch_data_1[0] < switch_data_2[0]
    elif switch_data_1[1] != switch_data_2[1]:
        return switch_data_1[1] < switch_data_2[1]
    elif switch_data_1[2] != switch_data_2[2]:
        return switch_data_1[2] < switch_data_2[2]

    return False


def read_graph_data(filename):

    switches = []
    connections = []

    f = open(filename, 'r')

    first_line = [eval(i) for i in f.readline().split()]
    number_of_switches = first_line[0]
    number_of_connections = first_line[1]

    for x in range(number_of_switches):
        switch_data = [eval(i) for i in f.readline().split()]
        switches.append(switch_data)

    switches = sorted(switches, key=lambda x: x[3])

    for x in range(number_of_connections):
        connection_data = [eval(i) for i in f.readline().split()]

        if not is_sorted_low_to_high(switches[connection_data[0]], switches[connection_data[1]]):
            connection_data[0], connection_data[1] = connection_data[1], connection_data[0]

        connections.append(connection_data)

    f.close()

    return switches, connections


def display_network(switches, connections):

    # we need to separate the X,Y,Z coordinates for Plotly
    x_switches = []  # x-coordinates of switches
    y_switches = []  # y-coordinates of switches
    z_switches = []  # z-coordinates of switches

    x_repeaters = []  # x-coordinates of repeaters
    y_repeaters = []  # y-coordinates of repeaters
    z_repeaters = []  # z-coordinates of repeaters

    # we need to create lists that contain the starting and ending coordinates of each connection
    x_connections = []  # x-coordinates of src and dest switches of connections
    y_connections = []  # y-coordinates of src and dest switches of connections
    z_connections = []  # z-coordinates of src and dest switches of connections

    # create lists holding midpoints that we will use to anchor text
    # x_midpoint_connections = []
    # y_midpoint_connections = []
    # z_midpoint_connections = []

    # create lists to store the labels of switches and repeaters
    switch_labels = []
    repeater_labels = []
    # midpoint_labels = []

    for switch_data in switches:
        x_switches.append(switch_data[0])
        y_switches.append(switch_data[1])
        z_switches.append(switch_data[2])
        switch_labels.append(f'Switch ID = {switch_data[3]}')

    for connection_data in connections:

        src_node = connection_data[0]
        dest_node = connection_data[1]
        number_of_repeaters = connection_data[2]

        x_src = x_switches[src_node]
        x_dest = x_switches[dest_node]
        y_src = y_switches[src_node]
        y_dest = y_switches[dest_node]
        z_src = z_switches[src_node]
        z_dest = z_switches[dest_node]

        x_coords_start_end_of_edge = [x_src, x_dest, None]
        x_connections += x_coords_start_end_of_edge
        # x_midpoint_edges.append(0.5 * (x_src + x_dest))

        y_coords_start_end_of_edge = [y_src, y_dest, None]
        y_connections += y_coords_start_end_of_edge
        # y_midpoint_edges.append(0.5 * (y_src + y_dest))

        z_coords_start_end_of_edge = [z_src, z_dest, None]
        z_connections += z_coords_start_end_of_edge
        # z_midpoint_edges.append(0.5 * (z_src + z_dest))

        # midpoint_labels.append(f'Number of Repeaters={connection_data[2]}')

        if number_of_repeaters != 0:

            x_diff_adder = (x_dest - x_src) / (number_of_repeaters+1)
            y_diff_adder = (y_dest - y_src) / (number_of_repeaters+1)
            z_diff_adder = (z_dest - z_src) / (number_of_repeaters+1)

            for itr in range(1, number_of_repeaters+1):
                x_repeaters.append(x_src + itr * x_diff_adder)
                y_repeaters.append(y_src + itr * y_diff_adder)
                z_repeaters.append(z_src + itr * z_diff_adder)
                repeater_labels.append(f'Repeater ID = {connection_data[0]}_{connection_data[1]}_{itr}')

    # trace_weights = go.Scatter3d(x=x_midpoint_edges, y=y_midpoint_edges, z=z_midpoint_edges,
    #                              mode='markers',
    #                              marker=dict(color='rgb(255,0,0)', size=1),
    #                              # set the same color as for the edge lines
    #                              text=midpoint_labels, hoverinfo='text')

    # create a trace for the edges
    trace_edges = go.Scatter3d(
        x=x_connections,
        y=y_connections,
        z=z_connections,
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none')

    # create a trace for the switches
    trace_switches = go.Scatter3d(
        x=x_switches,
        y=y_switches,
        z=z_switches,
        mode='markers',
        text=switch_labels,
        marker=dict(symbol='circle',
                    size=20,
                    color='skyblue')
    )

    # create a trace for the repeaters
    trace_repeaters = go.Scatter3d(
        x=x_repeaters,
        y=y_repeaters,
        z=z_repeaters,
        mode='markers',
        text=repeater_labels,
        marker=dict(symbol='circle',
                    size=10,
                    color='red')
    )

    # Include the traces we want to plot and create a figure
    # data = [trace_edges, trace_switches, trace_weights]
    # data = [trace_edges, trace_switches, trace_repeaters, trace_weights]
    data = [trace_edges, trace_switches, trace_repeaters]
    fig = go.Figure(data=data)

    fig.show()


switches, connections = read_graph_data('./../input/topology.txt')
display_network(switches, connections)
