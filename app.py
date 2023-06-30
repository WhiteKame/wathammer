import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import random
import re

from index import index


# ...你的模拟代码，如simulate函数...



app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                ],
                )

app.layout = html.Div([index])


@app.callback(
    Output('simulation-graph', 'figure'),
    [Input('run-button', 'n_clicks'),
     Input('hit_value', 'value'),
     Input('wound_value', 'value'),
     Input('armor_value', 'value'),
     Input('pain_value', 'value'),
     Input('reroll_hits', 'value'),
     Input('reroll_wounds', 'value'),
     Input('reroll_hit1', 'value'),
     Input('combo_strike', 'value')
     ],  # 改变这里
    [State('attack_input', 'value'),
     State('damage_value', 'value')]
)
def update_graph(n_clicks, hit_value, wound_value, armor_value, pain_value, reroll_hits, reroll_wounds, reroll_hit1,
                 combo_strike, attack_input, damage_value):
    if n_clicks is None:  # 刚开始的时候不执行模拟
        return go.Figure()

    reroll_hits = True if reroll_hits else False
    reroll_wounds = True if reroll_wounds else False
    reroll_hit1 = True if reroll_hit1 else False
    combo_strike = True if combo_strike else False

    # Process the input values
    attack_value = process_input_value(attack_input)
    damage_value = process_input_value(damage_value)

    # Run multiple simulations and get the results
    num_simulations = 10000
    results = [simulate(
        attack_value,
        hit_value,
        wound_value,
        armor_value,
        damage_value,
        pain_value,
        reroll_hits,
        reroll_wounds,
        reroll_hit1,
        combo_strike) for _ in range(num_simulations)]

    # 创建子图
    fig = make_subplots(rows=4, cols=1, subplot_titles=('成功命中', '成功造伤', '未过保护', '最终伤害'),
                        vertical_spacing=0.1)

    # 对于每个子图，添加柱状图
    for i, title in enumerate(['成功命中', '成功造伤', '未过保护', '最终伤害'], 1):
        data = [res[i - 1] for res in results]  # 取出对应的结果数据
        # 创建整数 bins
        bins = np.arange(min(data), max(data) + 2)  # 我们需要包括最大值，所以+2
        # 计算频率和 bin 的边界
        counts, bins = np.histogram(data, bins=bins, density=True)
        # 添加 Bar 图
        fig.add_trace(go.Bar(x=bins[:-1], y=counts, name=title), row=i, col=1)

    # 更新图形的外观
    fig.update_layout(
        height=1000,  # 设置图形的高度
        title_text="模拟结果",  # 设置图形的标题
    )

    return fig

@app.callback(
    [Output('attack_input', 'value'),
     Output('hit_value', 'value'),
     Output('wound_value', 'value'),
     Output('armor_value', 'value'),
     Output('pain_value', 'value'),
     Output('damage_value', 'value'),
     Output('reroll_hits', 'value'),
     Output('reroll_wounds', 'value'),
     Output('reroll_hit1', 'value'),
     Output('combo_strike', 'value')],
    [Input('reset-button', 'n_clicks')]
)
def reset_values(n):
    if n is None:
        # prevent the callbacks to be executed when the dashboard starts
        raise PreventUpdate
    else:
        return 4, 4, 4, 4, 7, 1, False, False, False, False  # replace these values with your default values


if __name__ == '__main__':
    app.run_server(debug=True)
