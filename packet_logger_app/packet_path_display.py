# from dash import dcc, html
from dash.dependencies import Input, Output, State


def func_of_packet_display(switches):
    from packet_logger_app import packet_log_reader as plr

    packet_id = 1  # int(get_packet_value())

    packet_details = plr.read_packet_log('input_files/packet_logger.txt')
    number_of_clocks = len(packet_details[packet_id])
    co_ordinates_collecter = []
    coordinates = None

    for x in packet_details[packet_id]:
        node_id = x[1]
        dir_id = x[2]
        buffer_id = x[3]
        position = x[4]

        for switch_data in switches:
            if node_id == switch_data[3]:
                coordinates = [switch_data[0], switch_data[1], switch_data[2]]
        dif = position * 2 / number_of_clocks
        match dir_id:
            case 0:
                coordinates[0] += dif
            case 1:
                coordinates[0] -= dif
            case 2:
                coordinates[1] += dif
            case 3:
                coordinates[1] -= dif
            case 4:
                coordinates[2] += dif
            case 5:
                coordinates[2] -= dif
        co_ordinates_collecter.append(coordinates)

    '''for x in co_ordinates_collecter:
        print(x)'''
    return co_ordinates_collecter
