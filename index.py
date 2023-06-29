from dash import dcc, html
import dash_bootstrap_components as dbc

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

index = html.Div([
    html.H1('甲鱼的数学战锤'),

    # dbc.Row([
    #     dbc.Col([
    #
    #     ], width=4),
    # ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P('输入攻击次数:'),
                dbc.Input(id='attack_input', className='input_name', type='text', value=4),
                html.P('输入单次伤害:'),
                dbc.Input(id='damage_value', className='input_name', type='text', value=1),
                dbc.Button('运行', id='run-button', color='primary', className='me-1 align-items-center'),
            ],
                className="h-100 p-5 text-white bg-dark rounded-3", ),
        ]),
        dbc.Col([
            html.Div([
                html.P('输入命中值:'),
                # dcc.Input(id='hit_value', type='number', value=4),
                dcc.Slider(2, 6, 1,
                           value=4,
                           id='hit_value'
                           ),
                html.P('输入造伤值:'),
                # dcc.Input(id='wound_value', type='number', value=4),
                dcc.Slider(2, 6, 1,
                           value=4,
                           id='wound_value'
                           ),
                html.P('输入保护值:'),
                # dcc.Input(id='armor_value', type='number', value=4),
                dcc.Slider(2, 7, 1,
                           value=4,
                           marks={
                               2: {'label': '2'},
                               3: {'label': '3'},
                               4: {'label': '4'},
                               5: {'label': '5'},
                               6: {'label': '6'},
                               7: {'label': '过穿', 'style': {'color': '#f50'}}
                           },
                           id='armor_value',
                           included=True
                           ),
                html.P('输入不怕疼:'),
                # dcc.Input(id='pain_value', type='number', value=7),
                dcc.Slider(2, 7, 1,
                           value=7,
                           marks={
                               2: {'label': '2'},
                               3: {'label': '3'},
                               4: {'label': '4'},
                               5: {'label': '5'},
                               6: {'label': '6'},
                               7: {'label': "没有", 'style': {'color': '#f50'}}
                           },
                           id='pain_value',
                           included=True
                           ),
            ]),
        ],
            className="h-100 p-5 bg-light border rounded-3",
        ),
        dbc.Col([
            html.Div([
                dcc.Tabs([

                    dcc.Tab(label='通用特效', children=[
                        html.Div([
                            dbc.Checkbox(id="reroll_hits",
                                         label="全重投命中",
                                         value=False, ),
                            dbc.Checkbox(id="reroll_hit1",
                                         label="重投命中1",
                                         value=False, ),
                            dbc.Checkbox(id="reroll_wounds",
                                         label="全重投造伤",
                                         value=False, )
                        ], className="input_name"),
                    ], style=tab_style, selected_style=tab_selected_style, className="rounded-3"),

                    dcc.Tab(label='武器特效', children=[
                        html.Div([
                            dbc.Checkbox(id="combo_strike",
                                         label="连击1",
                                         value=False, )
                        ], className="input_name"),
                    ], style=tab_style, selected_style=tab_selected_style, className="rounded-3"),
                    # dbc.InputGroup(
                    #     [
                    #         dbc.InputGroupText(dbc.Checkbox()),
                    #         dbc.InputGroupText("连击"),
                    #         dbc.Input(placeholder="数量", type="number"),
                    #     ],
                    #     className="mb-3",
                    # ),
                ], style=tabs_styles),
            ],
                className="h-100 p-5 bg-light border rounded-3",
            ),
        ]),
    ]),
    html.Div([
        dcc.Graph(id='simulation-graph')
    ]),
])
