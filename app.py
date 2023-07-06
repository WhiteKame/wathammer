import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots

from dice_input import process_input_value
from index import layout
from params import DiceParameters
from simulate import simulate

app = dash.Dash(__name__,
                title='Wathammer',
                update_title='Loading...',
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                ],
                )

app.layout = html.Div([layout])


def process_results(results):
    # 创建子图
    fig = make_subplots(rows=5, cols=1, subplot_titles=('成功命中', '成功造伤', '未过保护', '致命伤害', '最终受到伤害'),
                        vertical_spacing=0.1)

    # 对于每个子图，添加柱状图
    for i, title in enumerate(['成功命中', '成功造伤', '未过保护', '致命伤害', '最终受到伤害'], 1):
        data = [res[i - 1] for res in results]  # 取出对应的结果数据
        # 创建整数 bins
        bins = np.arange(min(data), max(data) + 2)  # 我们需要包括最大值，所以+2
        # 计算频率和 bin 的边界
        counts, bins = np.histogram(data, bins=bins, density=True)
        # 添加 Bar 图
        fig.add_trace(go.Bar(x=bins[:-1], y=counts, name=title), row=i, col=1)

    return fig


# 生成图表
@app.callback(
    Output('simulation-graph', 'figure'),
    [Input('run-button', 'n_clicks'),
     # 数值输入
     Input('hit_value', 'value'),
     Input('wound_value', 'value'),
     Input('armor_value', 'value'),
     Input('pain_value', 'value'),
     # 修正输入
     Input('hit_modify', 'value'),
     Input('wound_modify', 'value'),
     Input('armor_modify', 'value'),
     # 特殊规则
     Input('reroll_hits', 'value'),
     Input('reroll_wounds', 'value'),
     Input('reroll_hit1', 'value'),
     Input('combo_strike', 'value'),
     Input('mortal_wound', 'value'),
     Input('lethal_hits', 'value'),
     Input('anti', 'value')
     ],  # 改变这里
    [State('attack_input', 'value'),
     State('damage_value', 'value')]
)
def update_graph(n_clicks,
                 # 数值输入
                 hit_value, wound_value, armor_value, pain_value,
                 # 修正输入
                 hit_modify, wound_modify, armor_modify,
                 # 特殊规则
                 reroll_hits, reroll_wounds, reroll_hit1, combo_strike, mortal_wound, lethal_hits, anti,
                 # 攻击属性
                 attack_input, damage_value):
    dice_params = DiceParameters(
        hit_value=hit_value,
        wound_value=wound_value,
        armor_value=armor_value,
        pain_value=pain_value,
        hit_modify=hit_modify,
        wound_modify=wound_modify,
        armor_modify=armor_modify,
        reroll_hits=reroll_hits,
        reroll_wounds=reroll_wounds,
        reroll_hit1=reroll_hit1,
        combo_strike=combo_strike,
        mortal_wound=mortal_wound,
        lethal_hits=lethal_hits,
        anti=anti,
        attack_input=attack_input,
        damage_value=damage_value)

    if n_clicks is None:  # 刚开始的时候不执行模拟
        return go.Figure()

    if dice_params.attack_input == '' or dice_params.damage_value == '':
        return go.Figure()  # 如果输入是空字符串，则返回一个空的图表

    # Process the input values
    attack_value = process_input_value(dice_params.attack_input)
    damage_value = process_input_value(dice_params.damage_value)

    # Run multiple simulations and get the results
    num_simulations = 10000
    results = [simulate(attack_value, dice_params) for _ in range(num_simulations)]

    # Process the results and create the figure
    fig = process_results(results)

    # 更新图形的外观
    fig.update_layout(
        height=1000,  # 设置图形的高度
        title_text="模拟结果",  # 设置图形的标题
    )

    return fig


# 重置数值
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
     Output('combo_strike', 'value'),
     Output('mortal_wound', 'value'),
     Output('lethal_hits', 'value'),
     Output('anti', 'value')
     ],
    [Input('reset-button', 'n_clicks')]
)
def reset_values(n):
    if n is None:
        # prevent the callbacks to be executed when the dashboard starts
        raise PreventUpdate
    else:
        return '', 4, 4, 4, 7, '', False, False, False, False, False, False, False, False
        # replace these values with your default values


if __name__ == '__main__':
    app.run_server(debug=True)
