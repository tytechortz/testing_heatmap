import dash
from dash import html, dcc 
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import holoviews as hv
from holoviews.operation import histogram
from holoviews.operation.datashader import datashade as ds
from datashader.utils import lnglat_to_meters 
from holoviews.plotting.plotly.dash import to_dash
from holoviews.selection import link_selections

from plotly import colors






# Mapbox token (replace with your own token string)
mapbox_access_token = open(".mapbox_token").read()


df = pd.read_csv('/Users/jamesswank/Desktop/TestingData_coordinates.csv')
# print(df)
df2 = df.loc[:, 'geolongitude'], df.loc[:, 'geolatitude'] = lnglat_to_meters(df.geolongitude,df.geolatitude)
points = hv.Points(df2, ["geolatitude", "geolongitude"])
shaded = ds(points, cmap=colors.sequential.Plasma)
tiles = hv.Tiles().opts(
    mapboxstyle="light", accesstoken=mapbox_access_token,
    height=500, width=500, padding=0,
)

lnk_sel = link_selections.instance()
linked_map = lnk_sel(tiles * shaded)

# linked_hist = lnk_sel(hist)

# linked_hist.opts(margins=(60, 40, 30, 30))
linked_map.opts(margins=(30, 30, 30, 30))

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True
server = app.server

components = to_dash(
    app, [linked_map], reset_button=True, button_class=dbc.Button,
)



def get_layout():
    return dbc.Container([
    html.H1("COVID-19 Tests", style={"padding-top": 40}),
    html.Hr(),
    dbc.Row([
        dbc.Col(children=[dbc.Card([
            dbc.CardHeader("Test Locations"),
            dbc.CardBody(children=[
                components.graphs[0],
            ])])]),
        # dbc.Col(children=[dbc.Card([
        #     dbc.CardHeader("Fair Amount"),
        #     dbc.CardBody(children=[
        #         components.graphs[1]
        #     ])])])
    ]),
    html.Div(style={"margin-top": 10}, children=components.resets[0]),
    components.store,
])




app.layout = get_layout


if __name__ == '__main__':
    app.run_server(port=8000,debug=True)