import random
from dice_input import process_dice_input, process_input_value


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
