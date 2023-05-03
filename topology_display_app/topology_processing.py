def calc_distance(src_switch, dest_switch):
    x_diff = dest_switch[0] - src_switch[0]
    if x_diff > 0:
        return x_diff, 0
    elif x_diff < 0:
        return -1 * x_diff, 1

    y_diff = dest_switch[1] - src_switch[1]
    if y_diff > 0:
        return y_diff, 2
    elif y_diff < 0:
        return -1 * y_diff, 3

    z_diff = dest_switch[2] - src_switch[2]
    if z_diff > 0:
        return z_diff, 4
    elif z_diff < 0:
        return -1 * z_diff, 5

    return 0, -1


def topology_processing(switches, connections):
    # Store the coordinates tuple for switches and repeaters
    node_coordinates = []
    node_limits = []

    for switch_data in switches:
        node_coordinates.append([switch_data[0], switch_data[1], switch_data[2]])
        node_limits.append([0] * 6)

    for connection_data in connections:

        src_switch_id = connection_data[0]
        dest_switch_id = connection_data[1]
        number_of_repeaters = connection_data[2]

        dist_src_dest, dir_src_dest = calc_distance(switches[src_switch_id], switches[dest_switch_id])
        dir_dest_src = dir_src_dest

        if dir_dest_src % 2 == 0:
            dir_dest_src = dir_dest_src + 1
        else:
            dir_dest_src = dir_dest_src - 1

        limit = (0.5 * dist_src_dest) / (number_of_repeaters + 1)
        node_limits[src_switch_id][dir_src_dest] = limit
        node_limits[dest_switch_id][dir_dest_src] = limit

        if number_of_repeaters == 0:
            continue

        x_src_switch = switches[src_switch_id][0]
        y_src_switch = switches[src_switch_id][1]
        z_src_switch = switches[src_switch_id][2]

        x_dest_switch = switches[dest_switch_id][0]
        y_dest_switch = switches[dest_switch_id][1]
        z_dest_switch = switches[dest_switch_id][2]

        x_diff_adder = (x_dest_switch - x_src_switch) / (number_of_repeaters + 1)
        y_diff_adder = (y_dest_switch - y_src_switch) / (number_of_repeaters + 1)
        z_diff_adder = (z_dest_switch - z_src_switch) / (number_of_repeaters + 1)

        x_prev_node = x_src_switch
        y_prev_node = y_src_switch
        z_prev_node = z_src_switch

        for itr in range(1, number_of_repeaters + 1):
            # Compute coordinates of curr node using prev node
            x_curr_node = x_prev_node + x_diff_adder
            y_curr_node = y_prev_node + y_diff_adder
            z_curr_node = z_prev_node + z_diff_adder

            node_coordinates.append([x_curr_node, y_curr_node, z_curr_node])

            curr_node_limit = [0] * 6
            curr_node_limit[dir_src_dest] = limit
            curr_node_limit[dir_dest_src] = limit
            node_limits.append(curr_node_limit)

            x_prev_node = x_curr_node
            y_prev_node = y_curr_node
            z_prev_node = z_curr_node

    return node_coordinates, node_limits
