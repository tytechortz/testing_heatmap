import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pyproj import Transformer

import pandas as pd


df = pd.read_csv('/Users/jamesswank/Desktop/TestingData_coordinates.csv')


transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
x_3857, y_3857 = transformer.transform(df.geolatitude.values, df.geolongitude.values)
df = df.assign(x_3857=x_3857, y_3857=y_3857)

print(df)