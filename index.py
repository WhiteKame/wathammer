from dash import dcc, html
import dash_bootstrap_components as dbc

index = html.Div([
    html.H1('甲鱼的数学战锤'),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.P('输入攻击次数:'),
                dbc.Input(id='attack_input', className='input_name', type='text', placeholder='输入x, xD6, xD6+x'),
                html.P('输入单次伤害:'),
                dbc.Input(id='damage_value', className='input_name', type='text', placeholder='输入x, xD6, xD6+x'),
                dbc.Button('运行', id='run-button', color='primary'),
                dbc.Button('重置', id='reset-button', color='light')
            ],
                className="h-100 p-5 text-white bg-dark rounded-3 mb-3", ),
        ],
            className="mb-3", xs=12, md=4),
        dbc.Col([
            html.Div([
                dbc.Tabs([
                    dbc.Tab(
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
                                           2: {'label': '2+'},
                                           3: {'label': '3+'},
                                           4: {'label': '4+'},
                                           5: {'label': '5+'},
                                           6: {'label': '6+'},
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
                                           2: {'label': '2+'},
                                           3: {'label': '3+'},
                                           4: {'label': '4+'},
                                           5: {'label': '5+'},
                                           6: {'label': '6+'},
                                           7: {'label': "没有", 'style': {'color': '#f50'}}
                                       },
                                       id='pain_value',
                                       included=True
                                       ),
                        ]), label='数值'
                    ),
                    dbc.Tab(
                        html.Div([
                            html.P('输入命中修正:'),
                            dcc.Slider(-1, 1, 1,
                                       value=0,
                                       marks={
                                           -1: {'label': '-1'},
                                           0: {'label': '0'},
                                           1: {'label': '+1'}
                                       },
                                       id='hit_modify'
                                       ),
                            html.P('输入造伤修正:'),
                            dcc.Slider(-1, 1, 1,
                                       value=0,
                                       marks={
                                           -1: {'label': '-1'},
                                           0: {'label': '0'},
                                           1: {'label': '+1'}
                                       },
                                       id='wound_modify'
                                       ),
                            html.P('输入保护修正:'),
                            dcc.Slider(-1, 1, 1,
                                       value=0,
                                       marks={
                                           -1: {'label': '-1'},
                                           0: {'label': '0'},
                                           1: {'label': '+1'}
                                       },
                                       id='armor_modify'
                                       ),
                        ]), label='修正'
                    ),
                ]),
            ], className="h-100 p-5 bg-light border rounded-3 mb-3"),
        ],
            className="mb-3", xs=12, md=4
        ),
        dbc.Col([
            html.Div([
                dbc.Tabs([
                    dbc.Tab(html.Div([
                        dbc.Checkbox(id="reroll_hits",
                                     label="全重投命中",
                                     value=False, ),
                        dbc.Checkbox(id="reroll_hit1",
                                     label="重投命中1",
                                     value=False, ),
                        dbc.Checkbox(id="reroll_wounds",
                                     label="全重投造伤",
                                     value=False, )
                    ], className="input_name"), label='通用特效'
                    ),

                    dbc.Tab(
                        html.Div([
                            dbc.Checkbox(id="combo_strike",
                                         label="连击1",
                                         value=False, )
                        ], className="input_name"),
                        label='武器特效'),
                ]),
            ],
                className="h-100 p-5 bg-light border rounded-3 mb-3",
            ),
        ],
            className="mb-3", xs=12, md=4),
    ]),
    html.Div([
        dcc.Graph(id='simulation-graph')
    ]),
])
