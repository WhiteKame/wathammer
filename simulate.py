from dice_input import process_dice_input
from function import roll_dice


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
