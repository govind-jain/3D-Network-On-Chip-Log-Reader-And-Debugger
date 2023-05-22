import plotly.graph_objs as go


def packet_path_display(topology_display_fig, number_of_switches, packet_co_ordinates_at_different_intervals):
    last_node_id = number_of_switches - 1

    x_snapshot_output_buffer = []
    y_snapshot_output_buffer = []
    z_snapshot_output_buffer = []

    x_snapshot_input_buffer = []
    y_snapshot_input_buffer = []
    z_snapshot_input_buffer = []

    snapshot_output_labels = []
    snapshot_input_labels = []

    for snap_data in packet_co_ordinates_at_different_intervals:

        node_type_identifier = None
        if snap_data[6] > last_node_id:
            node_type_identifier = 'R'
        else:
            node_type_identifier = 'S'

        if snap_data[3] == 1:
            x_snapshot_output_buffer.append(snap_data[0])
            y_snapshot_output_buffer.append(snap_data[1])
            z_snapshot_output_buffer.append(snap_data[2])
            snapshot_output_labels.append(f'Clock_Cycle = {snap_data[4]} | Pos = {snap_data[5]} | Node_Id = {snap_data[6]}({node_type_identifier}) | Type = OP | Dir = {snap_data[7]}')
        else:
            x_snapshot_input_buffer.append(snap_data[0])
            y_snapshot_input_buffer.append(snap_data[1])
            z_snapshot_input_buffer.append(snap_data[2])
            snapshot_input_labels.append(f'Clock_Cycle = {snap_data[4]} | Pos = {snap_data[5]} | Node_Id = {snap_data[6]}({node_type_identifier}) | Type = IP | Dir = {snap_data[7]}')

    trace_snapshot_output_buffer = go.Scatter3d(
        x=x_snapshot_output_buffer,
        y=y_snapshot_output_buffer,
        z=z_snapshot_output_buffer,
        mode='markers',
        text=snapshot_output_labels,
        hovertemplate='%{text}<extra></extra>',
        marker=dict(symbol='circle',
                    size=3,
                    color='green')
    )

    topology_display_fig.add_trace(trace_snapshot_output_buffer)

    trace_snapshot_input_buffer = go.Scatter3d(
        x=x_snapshot_input_buffer,
        y=y_snapshot_input_buffer,
        z=z_snapshot_input_buffer,
        mode='markers',
        text=snapshot_input_labels,
        hovertemplate='%{text}<extra></extra>',
        marker=dict(symbol='circle',
                    size=3,
                    color='blue')
    )

    topology_display_fig.add_trace(trace_snapshot_input_buffer)

    return topology_display_fig
