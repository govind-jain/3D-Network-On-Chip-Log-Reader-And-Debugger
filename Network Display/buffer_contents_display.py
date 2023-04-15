import plotly.graph_objs as go


def buffer_contents_display(node_buffer_contents):
    # we need to separate the X,Y,Z coordinates for Plotly
    x_packets = []  # x-coordinates of switches
    y_packets = []  # y-coordinates of switches
    z_packets = []  # z-coordinates of switches