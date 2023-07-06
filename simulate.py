import copy

from dice_input import process_dice_input
from dice_roll import roll_dice


def simulate(attack_input, params):
    total_unprotected_count, total_hit_success, total_wound_success, total_damage_value, total_mortal_wound = 0, 0, 0, 0, 0
    total_extra_hit = 0

    attack_times = 0

    if 'D' in str(attack_input):
        attack_times = process_dice_input(attack_input)
    else:
        attack_times = int(attack_input)

    for _ in range(attack_times):
        hit_success, wound_success, unprotected_count, damage, extra_hit, mortal_wound = roll_dice(params)

        total_hit_success += hit_success
        total_wound_success += wound_success
        total_unprotected_count += unprotected_count
        total_damage_value += damage
        total_extra_hit += extra_hit
        total_mortal_wound += mortal_wound

    for _ in range(total_extra_hit):
        # Create a new DiceParameters object for extra hits by copying the original params
        dice_params = copy.deepcopy(params)
        # Change the hit_value and combo_strike parameters
        dice_params.hit_value = 0
        dice_params.combo_strike = False

        # 将新的DiceParameters对象传递给roll_dice函数
        hit_success, wound_success, unprotected_count, damage, extra_hit, mortal_wound = roll_dice(dice_params)

        total_hit_success += hit_success
        total_wound_success += wound_success
        total_unprotected_count += unprotected_count
        total_damage_value += damage
        # Reset extra hit for each simulation
        total_extra_hit = 0
        total_mortal_wound += mortal_wound

    return total_hit_success, total_wound_success, total_unprotected_count, total_mortal_wound, total_damage_value
