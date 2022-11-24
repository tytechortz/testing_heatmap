import dash
from dash import dcc, html
import holoviews as hv
from holoviews.plotting.plotly.dash import to_dash
from holoviews.operation.datashader import datashade


mapbox_token = open(".mapbox_token").read()

def get_layout():
    return html.Div([
        html.H2('Hello World')
    ])



app = dash.Dash(__name__)
# components = to_dash(app, [overlay], reset_button=True)

app.layout = get_layout


if __name__ == '__main__':
    app.run_server(port=8000,debug=True)