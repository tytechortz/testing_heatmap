import dash
from dash import dcc, html



def get_layout():
    return html.Div([
        html.H2('Hello World')
    ])



app = dash.Dash(__name__)
components = to_dash(app, [overlay], reset_button=True)

app.layout = get_layout


if __name__ == '__main__':
    app.run_server(debug=True)