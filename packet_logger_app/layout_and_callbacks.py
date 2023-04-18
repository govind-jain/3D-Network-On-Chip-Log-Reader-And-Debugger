from dash import dcc, html
from dash.dependencies import Input, Output


# Write all the callbacks for this app inside the function
def register_packet_path_callbacks(app):
    # @app.callback(
    #     Output('packet-path-graph', 'figure'),
    #     [Input('show-packet-path', 'n_clicks')],
    #     [dash.dependencies.State('packet-id-input_files', 'value')])
    # def display_packet_path(n_clicks, packet_id):
    #     if n_clicks is None or packet_id is None:
    #         return go.Figure()
    #     packet_path = get_packet_path(packet_id)
    #     return create_packet_path_plot(nodes, packet_path)

    # Delete this line, written to avoid error for now
    return app
