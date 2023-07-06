from dash import dcc


def create_slider(id, min, max, step, value):
    return dcc.Slider(min, max, step, value=value, id=id)
