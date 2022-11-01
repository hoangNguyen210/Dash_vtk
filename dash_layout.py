import pandas as pd
import numpy as np
# from dash import html
# from dash import dcc
# import dash_html_components as html
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_core_components as dcc
# import dash_bootstrap_components as dbc

import vtk
import dash
import dash_vtk
import pyvista as pv
import dash_obj_in_3dmesh
from flask import Flask
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_vtk.utils import to_mesh_state
from dash_vtk.utils import presets
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input,Output
from dash import callback_context


load_figure_template('BOOTSTRAP')


###--------------Build the figures / dropdowns------------------------------------

APP_ID = 'fea_vtk'
x = np.random.sample(100)
y = np.random.sample(100)
z = np.random.choice(a = ['a','b','c'], size = 100)


df1 = pd.DataFrame({'x': x, 'y':y, 'z':z}, index = range(100))

fig1 = px.scatter(df1, x= x, y = y, color = z)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}



model_name = "img8" #.obj & .mtl files in data/obj

axis_template = {
    "showbackground": False,
    "visible" : False
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    "showlegend": False,
    'uirevision':'same_all_the_time', #this keeps camera position etc the same when data changes.
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectmode" : "data",
        "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}


# ========================================================================
sidebar = html.Div(
    [
        html.H2("3D FACE PRESENTATION"),
        html.Hr(),
        html.P(
            "Visualize 3D FACE with a click ", className="lead"
        ),
        dbc.Nav(
            [
                dbc.Row([
                            dbc.Col([
                                html.H3('Step 1: Upload your mesh'),
                                # upload for nodes
                                dcc.Store(id=f'{APP_ID}_store', data=[True]),
                                dcc.Upload(
                                    id=f'{APP_ID}_nodes_upload',
                                    multiple=False,
                                    children=[
                                        dbc.Col([
                                            # dbc.Label('Upload your IMAGE'),
                                            # html.Br(),
                                            dbc.Button('Image folder', color='primary',className="d-grid gap-2")
                                        ])
                                    ]),
                                html.Br(),
                                html.H3('Step 2: Fit to model'),
                                dcc.Upload(
                                    id=f'{APP_ID}_nodes_upload_2',
                                    multiple=False,
                                    children=[
                                        dbc.Col([
                                            # dbc.Label('Fit to the Model'),
                                            # html.Br(),
                                            dbc.Button('Model', color="info",className="d-grid gap-2")
                                        ])
                                    ]),
                                html.Br(),
                                html.H3('Step 3: Upload Ground-truth'),
                                dcc.Upload(
                                    id=f'{APP_ID}_nodes_upload_3',
                                    multiple=False,
                                    children=[
                                        dbc.Col([
                                            # dbc.Label('Fit to the Model'),
                                            # html.Br(),
                                            dbc.Button('Ground-truth', color="success",className="d-grid gap-2")
                                        ])
                                    ]),
                                html.Br(),
                                html.H3('Step 4: Calculate loss'),
                                dcc.Upload(
                                    id=f'{APP_ID}_nodes_upload_4',
                                    multiple=False,
                                    children=[
                                        dbc.Col([
                                            # dbc.Label('Fit to the Model'),
                                            # html.Br(),
                                            dbc.Button('Loss', color="warning",className="d-grid gap-2")
                                        ])
                                    ]),
                                
                            ]),



                ]),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
###---------------Create the layout of the app ------------------------

external_stylesheets = [
        dbc.themes.BOOTSTRAP,
        # dbc.themes.LUX
    ]
app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div(children = [
                dbc.Row(
                    [
                    dbc.Col(sidebar),
                    dbc.Col(
                    dcc.Graph(
                                id="graph1",
                                figure={
                                    "data": dash_obj_in_3dmesh.geometry_tools.import_geometry([model_name]),
                                    "layout": plot_layout,
                                },
                                style = {'margin-left':'5px', 'margin-top':'7px', 'margin-right':'5px'},
                                config={"scrollZoom": True}, # activates wheel thingy on mouse to zoom and wotnot
                    )),
                    dbc.Col(
                    dcc.Graph(
                                id="graph2",
                                figure={
                                    "data": dash_obj_in_3dmesh.geometry_tools.import_geometry([model_name]),
                                    "layout": plot_layout,
                                },
                                style = {'margin-left':'5px', 'margin-top':'7px', 'margin-right':'5px'},
                                config={"scrollZoom": True}, # activates wheel thingy on mouse to zoom and wotnot
                    ))
                ])
    ]
)



@app.callback(
    Output("output", "children"),
    Input("input", "value"),
    Input("show-image", "n_clicks"),
    prevent_initial_call=True,
)
def update_output(input, n_clicks):
    if not input:
        raise PreventUpdate

    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"].split(".")[0] != "show-image":
        raise PreventUpdate

    try:
        img = np.array(Image.open(f"assets/{input}"))
    except OSError:
        raise PreventUpdate

    fig = px.imshow(img, color_continuous_scale="gray")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    return dcc.Graph(figure=fig)



if __name__ == '__main__':
    app.run_server(port = 9001, debug=True)