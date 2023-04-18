from dash import dcc, html
from dash.dependencies import Input, Output


# Write all the callbacks for this app inside the function
def register_buffer_contents_callbacks(app):
    @app.callback(
        Output('buffer-contents', 'children'),
        [Input('clock-cycle-selector', 'value')])
    def display_buffer_contents(clock_cycle):
        print(clock_cycle)
        return html.Hr()

    #     buffer_contents = get_buffer_contents(node_id, clock_cycle)
    #     return create_buffer_contents_plot(buffer_contents)


def get_switch_section_layout(layer_array, switch_array, max_clock_cycle):
    switch_section_layout = [
        html.H2('Switch logger', style={'text-align': 'center', 'padding': '20px', 'font-size': '30px'}),
        html.Div([
            html.Div([
                html.Label("Select Layer:"),
                dcc.Dropdown(
                    id='layer-selector',
                    options=layer_array
                )
            ], style={'width': '12%', 'display': 'inline-block', 'padding': '0 20px'}),
            html.Div([
                html.Label("Select Node:"),
                dcc.Dropdown(
                    id='switch-selector',
                    options=switch_array
                )
            ], style={'width': '12%', 'display': 'inline-block', 'padding': '0 20px'}),
            html.Div([
                html.Label("Select Clock Cycle:"),
                dcc.Slider(
                    id='clock-cycle-selector',
                    min=0,
                    max=max_clock_cycle,
                    value=0,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={'width': '45%', 'display': 'inline-block', 'padding': '0 20px'}),
            html.Div([
                html.Button("Go", id="show-buffer-contents")
            ], style={'width': '10%', 'display': 'inline-block', 'padding': '0 20px'}),
        ], style={'margin': '40px'}),
        html.Div(id='buffer-contents', style={'display': 'none'}), ]

    return switch_section_layout
