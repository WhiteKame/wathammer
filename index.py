import dash_bootstrap_components as dbc
from dash import dcc, html

from function import create_slider

# 输入攻击次数和伤害
attack_input = dbc.Input(
    id='attack_input',
    className='input_name',
    type='text',
    placeholder='输入 {x} {xD6} {xD6+x}'
)

damage_input = dbc.Input(
    id='damage_value',
    className='input_name',
    type='text',
    placeholder='输入 {x} {xD6} {xD6+x}'
)

# 按钮
run_button = dbc.Button('运行', id='run-button', color='primary')
reset_button = dbc.Button('重置', id='reset-button', color='light')
buttons_div = html.Div([
    run_button,
    reset_button
], className="d-flex justify-content-between")

attack_input_div = html.Div([
    html.P('输入攻击次数:'),
    attack_input,
    html.P('输入单次伤害:'),
    damage_input,
    buttons_div,
], className="p-3 text-white bg-dark rounded-3 mb-3")

# 输入数据表的内容
hit_input = create_slider('hit_value', 2, 6, 1, 4)
wound_input = create_slider('wound_value', 2, 6, 1, 4)

save_input = dcc.Slider(
    2, 7, 1,
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
)

pain_input = dcc.Slider(
    2, 7, 1,
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
)

datasheet_input_div = html.Div([
    html.P('输入命中值:'),
    hit_input,
    html.P('输入造伤值:'),
    wound_input,
    html.P('输入保护值:'),
    save_input,
    html.P('输入不怕疼:'),
    pain_input,
])

# 输入修正值
hit_modify_input = dcc.Slider(
    -1, 1, 1,
    value=0,
    marks={
        -1: {'label': '-1'},
        0: {'label': '0'},
        1: {'label': '+1'}
    },
    id='hit_modify'
)

wound_modify_input = dcc.Slider(
    -1, 1, 1,
    value=0,
    marks={
        -1: {'label': '-1'},
        0: {'label': '0'},
        1: {'label': '+1'}
    },
    id='wound_modify'
)

save_modify_input = dcc.Slider(
    -1, 1, 1,
    value=0,
    marks={
        -1: {'label': '-1'},
        0: {'label': '0'},
        1: {'label': '+1'}
    },
    id='armor_modify'
)

modify_input_div = html.Div([
    html.P('输入命中修正:'),
    hit_modify_input,
    html.P('输入造伤修正:'),
    wound_modify_input,
    html.P('输入保护修正:'),
    save_modify_input,
])

# 数值输入
data_input_div = html.Div([
    dbc.Tabs([
        dbc.Tab(datasheet_input_div, label="数值"),
        dbc.Tab(modify_input_div, label="修正")
    ])
])

# 通用特效
sp_rule = html.Div([
    dbc.Checkbox(id="reroll_hits",
                 label="全重投命中",
                 value=False, ),
    dbc.Checkbox(id="reroll_hit1",
                 label="重投命中1",
                 value=False, ),
    dbc.Checkbox(id="reroll_wounds",
                 label="全重投造伤",
                 value=False, )
], className="input_name")

# 特殊武器规则
sp_weapon_rule = html.Div([
    # dbc.Checkbox(id="combo_strike",
    #              label="连击1",
    #              value=False, ),
    dbc.RadioItems(
        options=[
            {"label": "无", "value": 0},
            {"label": "连击1", "value": 1},
            {"label": "连击2", "value": 2},
            {"label": "连击D3", "value": 'D3'},
        ],
        value=0,
        id="combo_strike",
        inline=True,
        className='mb-2',
    ),
    dbc.Checkbox(id="mortal_wound",
                 label="毁灭伤害",
                 value=False, ),
    dbc.Checkbox(id="lethal_hits",
                 label="致命一击",
                 value=False, ),
    html.P("针对:"),
    dbc.Select(
        options=[
            {"label": "无", "value": 7},
            {"label": "针对 2+", "value": 2},
            {"label": "针对 3+", "value": 3},
            {"label": "针对 4+", "value": 4},
            {"label": "针对 5+", "value": 5},
            {"label": "针对 6+", "value": 6},
        ],
        id="anti",
        value=7
    )
], className="input_name")

# 特殊规则输入
sp_rule_input_div = html.Div([
    dbc.Tabs([
        dbc.Tab(sp_rule, label="通用特效"),
        dbc.Tab(sp_weapon_rule, label="武器特效")
    ])
], className="p-3")

# 图表
graph_div = html.Div([
    dcc.Graph(id='simulation-graph')
], style={'height': '100vh', 'overflow': 'scroll'})

# 输出页
layout = html.Div([
    dbc.Row([
        dbc.Col([  # 左侧列
            html.H1('甲鱼的数学战锤 BETA v0.1'),
            html.P('QQ群 869510322'),
            dbc.Row([
                dbc.Col([
                    attack_input_div
                ]),
                dbc.Col([
                    sp_rule_input_div
                ])
            ], className='row-eq-height'),
            data_input_div
        ],
            xs=12, md=6),  # 调整列宽比例

        dbc.Col([  # 右侧列
            graph_div
        ],
            xs=12, md=6),  # 调整列宽比例
    ])
])
