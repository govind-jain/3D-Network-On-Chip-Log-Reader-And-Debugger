def read_packet_log(filepath):
    packet_dic = {}

    f = open(filepath, 'r')

    while True:
        line = f.readline().strip()
        if not line:
            break

        split_list = line.split(' ')
        packet_number = int(split_list[0][split_list[0].find('=') + 1:])
        clock_cycle = int(split_list[1][split_list[1].find('=') + 1:].strip())
        layer_id = int(split_list[2][split_list[2].find('=') + 1:].strip())
        node_id = int(split_list[3][split_list[3].find('=') + 1:].strip())
        dir_id = int(split_list[4][split_list[4].find('=') + 1:].strip())
        buffer_id = int(split_list[5][split_list[5].find('=') + 1:].strip())
        pos_idx = int(split_list[6][split_list[6].find('=') + 1:].strip())

        tup = (layer_id, node_id, dir_id, buffer_id, pos_idx, clock_cycle)

        if not (packet_number in packet_dic):
            packet_dic[packet_number] = []

        packet_dic[packet_number].append(tup)

    return packet_dic
