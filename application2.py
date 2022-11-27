import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os

import pandas as pd

import os
import time
from textwrap import dedent











# Colors
bgcolor = "#f3f3f1"  # mapbox light map land color
bar_bgcolor = "#b0bec5"  # material blue-gray 200
bar_unselected_color = "#78909c"  # material blue-gray 400
bar_color = "#546e7a"  # material blue-gray 600
bar_selected_color = "#37474f"  # material blue-gray 800
bar_unselected_opacity = 0.8



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

# def build_modal_info_overlay(id, side, content):
#     """
#     Build div representing the info overlay for a plot panel
#     """
#     div = html.Div(
#         [  # modal div
#             html.Div(
#                 [  # content div
#                     html.Div(
#                         [
#                             html.H4(
#                                 [
#                                     "Info",
#                                     html.Img(
#                                         id=f"close-{id}-modal",
#                                         src="assets/times-circle-solid.svg",
#                                         n_clicks=0,
#                                         className="info-icon",
#                                         style={"margin": 0},
#                                     ),
#                                 ],
#                                 className="container_title",
#                                 style={"color": "white"},
#                             ),
#                             dcc.Markdown(content),
#                         ]
#                     )
#                 ],
#                 className=f"modal-content {side}",
#             ),
#             html.Div(className="modal"),
#         ],
#         id=f"{id}-modal",
#         style={"display": "none"},
#     )

#     return 


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


# Create show/hide callbacks for each info modal
# for id in ["indicator", "radio", "map", "range", "created"]:

# @app.callback(
#     [Output(f"{id}-modal", "style"), Output(f"{id}-div", "style")],
#     [Input(f"show-{id}-modal", "n_clicks"), Input(f"close-{id}-modal", "n_clicks")],
# )
# def toggle_modal(n_show, n_close):
#     ctx = dash.callback_context
#     if ctx.triggered and ctx.triggered[0]["prop_id"].startswith("show-"):
#         return {"display": "block"}, {"zIndex": 1003}
#     else:
#         return {"display": "none"}, {"zIndex": 0}


# # Create clear/reset button callbacks
# @app.callback(
#     Output("map-graph", "relayoutData"),
#     [Input("reset-map", "n_clicks"), Input("clear-all", "n_clicks")],
# )
# def reset_map(*args):
#     return None


# @app.callback(
#     # Output("tests-histogram", "selectedData"),
#     [Input("clear-tests", "n_clicks"), Input("clear-all", "n_clicks")],
# )
# def clear_tests_hist_selections(*args):
#     return None

@app.callback(
    [
        Output("map-graph", "figure"),
        # Output("tests-histogram", "figure")
    ],
    [
        Input("map-graph", "relayoutData"),
        # Input("tests-histogram", "selectedData")
    ],
)
def update_plots(
    relayout_data,
    # selected_tests
):
    df = pd.read_csv('/Users/jamesswank/Desktop/TestingData_coordinates.csv')
    print(df)
    t0 = time.time()
    coordinates_4326 = relayout_data and relayout_data.get("mapbox._derived", {}).get(
        "coordinates", None
    )

    # if coordinates_4326:
    #     lons, lats = zip(*coordinates_4326)
    #     lon0, lon1 = max(min(lons), data_4326[0][0]), min(max(lons), data_4326[1][0])
    #     lat0, lat1 = max(min(lats), data_4326[0][1]), min(max(lats), data_4326[1][1])
    #     coordinates_4326 = [
    #         [lon0, lat0],
    #         [lon1, lat1],
    #     ]
    #     coordinates_3857 = epsg_4326_to_3857(coordinates_4326)
    #     # position = {}
    #     position = {
    #         "zoom": relayout_data.get("mapbox.zoom", None),
    #         "center": relayout_data.get("mapbox.center", None),
    #     }
    if coordinates_4326:
        lons, lats = zip(*coordinates_4326)
        lon0, lon1 = max(min(lons), df[0][0]), min(max(lons), df[1][0])
        lat0, lat1 = max(min(lats), df[0][1]), min(max(lats), df[1][1])
        coordinates_4326 = [
            [lon0, lat0],
            [lon1, lat1],
        ]
        coordinates_3857 = epsg_4326_to_3857(coordinates_4326)
        # position = {}
        position = {
            "zoom": relayout_data.get("mapbox.zoom", None),
            "center": relayout_data.get("mapbox.center", None),
    }
    else:
        position = {
            "zoom": 0.5,
            "pitch": 0,
            "bearing": 0,
            "center": {"lon": -104, "lat": 39},
        }
    #     coordinates_3857 = data_3857
    #     coordinates_4326 = data_4326

    # new_coordinates = [
    #     [coordinates_4326[0][0], coordinates_4326[1][1]],
    #     [coordinates_4326[1][0], coordinates_4326[1][1]],
    #     [coordinates_4326[1][0], coordinates_4326[0][1]],
    #     [coordinates_4326[0][0], coordinates_4326[0][1]],
    # ]

    # x_range, y_range = zip(*coordinates_3857)
    # x0, x1 = x_range
    # y0, y1 = y_range


    # Count the number of selected towers
    # n_selected = int(agg.sum())

    # Build indicator figure
    # n_selected_indicator = {
    #     "data": [
    #         {
    #             "type": "indicator",
    #             "value": n_selected,
    #             "number": {"font": {"color": "#263238"}},
    #         }
    #     ],
    #     "layout": {
    #         "template": template,
    #         "height": 150,
    #         "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
    #     },
    # }

    # if n_selected == 0:
    #     # Nothing to display
    #     lat = [None]
    #     lon = [None]
    #     customdata = [None]
    #     marker = {}
    #     layers = []
    # elif n_selected < 5000:
    #     # Display each individual point using a scattermapbox trace. This way we can
    #     # give each individual point a tooltip
    #     ddf_small_expr = " & ".join(
    #         [query_expr_xy]
    #         + [f"(radio in {selected_radio_categories})"]
    #         + query_expr_range_created_parts
    #     )
        # ddf_small = cell_towers_ddf.query(ddf_small_expr)
        # (
        #     lat,
        #     lon,
        #     radio,
        #     log10_range,
        #     description,
        #     mcc,
        #     net,
        #     created,
        #     status,
        # ) = dask.compute(
        #     ddf_small.lat,
        #     ddf_small.lon,
        #     ddf_small.radio,
        #     ddf_small.log10_range,
        #     ddf_small.Description,
        #     ddf_small.mcc,
        #     ddf_small.net,
        #     ddf_small.created,
        #     ddf_small.Status,
        # )


# Build map figure
    map_graph = {
        "data": [
            {
                "type": "scattermapbox",
                # "lat": geolatitude,
                # "lon": geolongitude,
                # "customdata": customdata,
                # "marker": marker,
                "hovertemplate": (
                    "<b>%{customdata[2]}</b><br>"
                    "MCC: %{customdata[3]}<br>"
                    "MNC: %{customdata[4]}<br>"
                    "radio: %{customdata[0]}<br>"
                    "range: %{customdata[1]:,} m<br>"
                    "created: %{customdata[5]}<br>"
                    "status: %{customdata[6]}<br>"
                    "longitude: %{lon:.3f}&deg;<br>"
                    "latitude: %{lat:.3f}&deg;<br>"
                    "<extra></extra>"
                ),
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

    # Use datashader to histogram range, created, and radio simultaneously
    # agg_tests = compute_test_hist(client)

    # Build test histogram
    # selected_test_counts = (
    #     agg_test.sel(log10_range=test_slice)
    #     .sum(["log10_range", "created"])
    #     .to_series()
    # )
    # tests_histogram = build_tests_histogram(
    #     selected_test_counts, selected_test is None
    # )
    print(f"Update time: {time.time() - t0}")

    return (
        # n_selected_indicator,
        map_graph,
        # radio_histogram,
        # range_histogram,
        # created_histogram,
    )

if __name__ == '__main__':
    app.run_server(port=8000,debug=True)