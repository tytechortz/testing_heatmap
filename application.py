import dash
from dash import html, dcc





# Mapbox token (replace with your own token string)
mapbox_access_token = open(".mapbox_token").read()


df = pd.read_csv('/Users/jamesswank/Python_projects/testing_heatmap/TestingData_coordinates.csv')


app.layout = get_layout


if __name__ == '__main__':
    app.run_server(port=8000,debug=True)