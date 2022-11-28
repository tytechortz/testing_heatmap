import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pyproj import Transformer

import pandas as pd


# Colors
bgcolor = "#f3f3f1"  # mapbox light map land color


df = pd.read_csv('/Users/jamesswank/Desktop/TestingData_coordinates.csv')


transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
x_3857, y_3857 = transformer.transform(df.geolatitude.values, df.geolongitude.values)
df = df.assign(x_3857=x_3857, y_3857=y_3857)

print(df)

# Figure template
row_heights = [150, 500, 300]
template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}

def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "template": template,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }

# Load mapbox token
mapbox_access_token = open(".mapbox_token").read()

# Build Dash layout
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            [
                "COVID-19 TESTING"
            ],
            style={"text-align": "left"}
        ),
        dcc.Graph(
            id="map-graph",
            figure=blank_fig(row_heights[1]),
        )
    ]
)




if __name__ == '__main__':
    app.run_server(port=8000,debug=True)