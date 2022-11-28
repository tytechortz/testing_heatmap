import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pyproj import Transformer

import pandas as pd


# Colors
bgcolor = "#f3f3f1"  # mapbox light map land color




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
print(mapbox_access_token)

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
        ),
        html.Div([
            dcc.RangeSlider(
                2017,2021,1, value=[2020,2022],
                id='years',
                marks={2020:'2020',2021:'2021',2022: '2022'},
            ),
        ],
            className='four columns'
        ),
        dcc.Store(id='testing-data', storage_type='memory'),
    ]
)

@app.callback(
    Output('testing-data', 'data'),
    Input('years', 'value'))
def get_testing_data(years):
    print(years)
    df = pd.read_csv('/Users/jamesswank/Desktop/TestingData_coordinates.csv')
    print(df)
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    x_3857, y_3857 = transformer.transform(df.geolatitude.values, df.geolongitude.values)
    df = df.assign(x_3857=x_3857, y_3857=y_3857)

    return df.to_json()

@app.callback(
    Output('map-graph', 'figure'),
    Input('map-graph', 'relayoutData'),
    Input('testing-data', 'data'))
def update_plots(relayout_data, test_data):
    df1 = pd.read_json(test_data)
    print(df1)

    position = {
            "zoom": 8,
            "pitch": 0,
            "bearing": 0,
            "center": {"lon": -104.8, "lat": 39.7},
        }

    # Build map figure
    map_graph = {
        "data": [
            {
                "type": "scattermapbox",
                "lat": df1.geolatitude,
                "lon": df1.geolongitude,
                # "customdata": customdata,
                # "marker": marker,
                # "hovertemplate": (
                #     "<b>%{customdata[2]}</b><br>"
                #     "MCC: %{customdata[3]}<br>"
                #     "MNC: %{customdata[4]}<br>"
                #     "radio: %{customdata[0]}<br>"
                #     "range: %{customdata[1]:,} m<br>"
                #     "created: %{customdata[5]}<br>"
                #     "status: %{customdata[6]}<br>"
                #     "longitude: %{lon:.3f}&deg;<br>"
                #     "latitude: %{lat:.3f}&deg;<br>"
                #     "<extra></extra>"
                # ),
            }
        ],
        "layout": {
            "template": template,
            "uirevision": True,
            "mapbox": {
                "style": "light",
                "accesstoken": mapbox_access_token,
                # "layers": layers,
            },
            "margin": {"r": 0, "t": 0, "l": 0, "b": 0},
            "height": 500,
            "shapes": [
                {
                    "type": "rect",
                    "xref": "paper",
                    "yref": "paper",
                    "x0": 0,
                    "y0": 0,
                    "x1": 1,
                    "y1": 1,
                    "line": {
                        "width": 2,
                        "color": "#B0BEC5",
                    },
                }
            ],
        },
    }

    map_graph["layout"]["mapbox"].update(position)


    return map_graph



if __name__ == '__main__':
    app.run_server(port=8000,debug=True)