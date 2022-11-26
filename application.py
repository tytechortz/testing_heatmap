import dash
from dash import html, dcc
import holoviews as hv
import plotly.express as px
from holoviews.plotting.plotly.dash import to_dash
from holoviews.operation.datashader import datashade
import pandas as pd
import numpy as np
from plotly.data import carshare
from plotly.colors import sequential
import datashader as ds
from colorcet import fire
import datashader.transfer_functions as tf
# from datashader.geo import lnglat_to_meters



# Mapbox token (replace with your own token string)
mapbox_access_token = open(".mapbox_token").read()

# print(mapbox_token)
# Convert from lon/lat to web-mercator easting/northing coordinates
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv')
df = pd.read_csv('/Users/jamesswank/Python_projects/testing_heatmap/TestingData_coordinates.csv')
# dff = df.query('Lat < 40.82').query('Lat > 40.70').query('Lon > -74.02').query('Lon < -73.91')
# from datashader import datashader.utils.lnglat_to_meters
# df.loc[:, 'geolatitude'], df.loc[:, 'geolongitude'] = lnglat_to_meters(df.geolatitude,df.geolongitude)
# print(df)

cvs = ds.Canvas(plot_width=1000, plot_height=1000)
agg = cvs.points(df, 'geolongitude', 'geolatitude')
# agg is an xarray object, see http://xarray.pydata.org/en/stable/ for more details
coords_lat, coords_lon = agg.coords['geolatitude'].values, agg.coords['geolongitude'].values
# Corners of the image, which need to be passed to mapbox
coordinates = [[coords_lon[0], coords_lat[0]],
               [coords_lon[-1], coords_lat[0]],
               [coords_lon[-1], coords_lat[-1]],
               [coords_lon[0], coords_lat[-1]]]

img = tf.shade(agg, cmap=fire)[::-1].to_pil()


# img = tf.shade(agg, cmap=fire)[::-1].to_pil()
# df_original = carshare()
# df_original["easting"], df_original["northing"] = hv.Tiles.lon_lat_to_easting_northing(
# df_original["centroid_lon"], df_original["centroid_lat"]
# )

# # Duplicate carshare dataframe with Gaussian noise to produce a larger dataframe
# df = pd.concat([df_original] * 5000)
# df["easting"] = df["easting"] + np.random.randn(len(df)) * 400
# df["northing"] = df["northing"] + np.random.randn(len(df)) * 400
# print(df)
# Build Dataset and graphical elements
# dataset = hv.Dataset(df)
# print(dataset)
# points = hv.Points(df, ["geolatitude", "geolongitude"]).opts(color="crimson")
# print(points)
tiles = hv.Tiles().opts(mapboxstyle="light", accesstoken=mapbox_access_token)
overlay = img
# overlay = tiles * datashade(points, cmap=sequential.Plasma)
# overlay.opts(
#     title="Mapbox Datashader with %d points" % len(df),
#     width=800,
#     height=500
# )
import plotly.express as px
# Trick to create rapidly a figure with mapbox axes
fig = px.scatter_mapbox(df[:1], lat='geolatitude', lon='geolongitude', zoom=12)
# Add the datashader image as a mapbox layer image
fig.update_layout(mapbox_style="carto-darkmatter",
                 mapbox_layers = [
                {
                    "sourcetype": "image",
                    "source": img,
                    "coordinates": coordinates
                }]
)
# fig.show()

# Build App
app = dash.Dash(__name__)
# components = to_dash(app, [overlay], reset_button=True)
# components = to_dash(app, reset_button=True)

app.layout = html.Div([
    dcc.Graph(figure=fig)
    # components.children
])


if __name__ == '__main__':
    app.run_server(port=8000,debug=True)