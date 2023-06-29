import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import re

from index import index


# ...你的模拟代码，如simulate函数...
def process_dice_input(dice_input):
    pattern = re.compile(r'(\d*)D(3|6)\+*(\d*)')
    match = pattern.match(dice_input)

    if match:
        dice_count = match.group(1)
        dice_value = int(match.group(2))
        if dice_count == '':  # Default to 1 if no dice count is provided
            dice_count = 1
        else:
            dice_count = int(dice_count)

        plus_value = match.group(3)
        if plus_value == '':  # Default to 0 if no plus value is provided
            plus_value = 0
        else:
            plus_value = int(plus_value)

        dice_output = sum(max(1, random.randint(1, dice_value)) for _ in range(dice_count)) + plus_value
    elif dice_input.isdigit():
        dice_output = int(dice_input)
    else:
        print(f"Invalid attack input: '{dice_input}'")
        raise ValueError("Invalid attack input. Please enter a number or a format like '3D6' or 'D6+1' or 'D3'.")

    return dice_output


def process_input_value(input_value):
    if isinstance(input_value, str):
        if 'D' in input_value:
            return input_value
        elif input_value.isdigit():
            return int(input_value)
        else:
            raise ValueError("Invalid input. Please enter a number or a format like '3D6'.")
    elif isinstance(input_value, int):
        return input_value
    else:
        raise ValueError("Invalid input. Please enter a number or a format like '3D6'.")


def roll_dice(hit_value, wound_value, armor_value, damage_value, pain_value, reroll_hits, reroll_wounds, reroll_hit1,
              combo_strike):
    hit_success, wound_success, protected_fail, damage = 0, 0, 0, 0
    extra_hit = 0

    # Roll for hit
    hit_roll = random.randint(1, 6)

    # If reroll for hit roll of 1 is allowed
    if hit_roll == 1 and reroll_hit1:
        hit_roll = random.randint(1, 6)
    # If reroll for failed hit roll is allowed
    elif hit_roll < hit_value and reroll_hits:
        hit_roll = random.randint(1, 6)

    if hit_roll >= hit_value:
        hit_success = 1
        if hit_roll == 6 and combo_strike:
            extra_hit = 1

    # Roll for wound
    if hit_success:
        wound_roll = random.randint(1, 6)
        if wound_roll >= wound_value:
            wound_success = 1
        elif reroll_wounds and wound_roll < wound_value:
            wound_roll = random.randint(1, 6)
            if wound_roll >= wound_value:
                wound_success = 1

    # Roll for armor save
    if wound_success:
        armor_roll = random.randint(1, 6)
        if armor_roll < armor_value:
            protected_fail = 1

    # Roll for not pain
    if protected_fail:
        if 'D' in str(damage_value):
            damage_result = process_dice_input(damage_value)
        else:
            damage_result = int(damage_value)

        if pain_value == 7:  # 不触发pain检测
            damage += damage_result
        else:  # 进行pain检测
            for _ in range(damage_result):  # check for not pain
                pain_roll = random.randint(1, 6)
                if pain_roll < pain_value:
                    damage += 1

    return hit_success, wound_success, protected_fail, damage, extra_hit


def simulate(attack_input, hit_value, wound_value, armor_value, damage_value, pain_value, reroll_hits, reroll_wounds,
             reroll_hit1, combo_strike):
    total_unprotected_count, total_hit_success, total_wound_success, total_damage_value = 0, 0, 0, 0
    total_extra_hit = 0

    attack_times = 0

    if 'D' in str(attack_input):
        attack_times = process_dice_input(attack_input)
    else:
        attack_times = int(attack_input)

    for _ in range(attack_times):
        hit_success, wound_success, unprotected_count, damage, extra_hit = roll_dice(hit_value, wound_value,
                                                                                     armor_value,
                                                                                     damage_value, pain_value,
                                                                                     reroll_hits,
                                                                                     reroll_wounds, reroll_hit1,
                                                                                     combo_strike)

        total_hit_success += hit_success
        total_wound_success += wound_success
        total_unprotected_count += unprotected_count
        total_damage_value += damage
        total_extra_hit += extra_hit

    for _ in range(total_extra_hit):
        # 额外命中
        hit_success, wound_success, unprotected_count, damage, extra_hit = roll_dice(0, wound_value,
                                                                                     armor_value,
                                                                                     damage_value, pain_value,
                                                                                     reroll_hits,
                                                                                     reroll_wounds, reroll_hit1,
                                                                                     "no")
        total_hit_success += hit_success
        total_wound_success += wound_success
        total_unprotected_count += unprotected_count
        total_damage_value += damage
        # Reset extra hit for each simulation
        total_extra_hit = 0

    return total_hit_success, total_wound_success, total_unprotected_count, total_damage_value


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([index])


@app.callback(
    Output('simulation-graph', 'figure'),
    [Input('run-button', 'n_clicks')],  # 改变这里
    [State('attack_input', 'value'),
     State('hit_value', 'value'),
     State('wound_value', 'value'),
     State('armor_value', 'value'),
     State('pain_value', 'value'),
     State('damage_value', 'value'),
     State('reroll_hits', 'value'),
     State('reroll_wounds', 'value'),
     State('reroll_hit1', 'value'),
     State('combo_strike', 'value')]
)
def update_graph(n_clicks, attack_input, hit_value, wound_value, armor_value, pain_value, damage_value, reroll_hits,
                 reroll_wounds, reroll_hit1, combo_strike):
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


if __name__ == '__main__':
    app.run_server(debug=True)
