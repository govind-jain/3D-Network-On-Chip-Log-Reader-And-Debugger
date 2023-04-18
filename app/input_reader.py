def is_sorted_low_to_high(switch_data_1, switch_data_2):
    if switch_data_1[0] != switch_data_2[0]:
        return switch_data_1[0] < switch_data_2[0]
    elif switch_data_1[1] != switch_data_2[1]:
        return switch_data_1[1] < switch_data_2[1]
    elif switch_data_1[2] != switch_data_2[2]:
        return switch_data_1[2] < switch_data_2[2]

    return False


def read_topology_config(filename):
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
