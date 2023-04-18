from dash import dcc, html


def get_topology_display_layout(topology_display_fig):
    topology_display_layout = [html.H2('Network Topology', style={'text-align': 'center', 'font-size': '30px'}),
                               dcc.Graph(id='network-graph', figure=topology_display_fig,
                                         style={'padding-bottom': '5%'})]
    return topology_display_layout
