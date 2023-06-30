import random
from dice_input import process_dice_input, process_input_value


def roll_for_hit(hit_value, reroll_hits, reroll_hit1, combo_strike):
    hit_roll = random.randint(1, 6)

    if hit_roll == 1 and reroll_hit1:
        hit_roll = random.randint(1, 6)
    elif hit_roll < hit_value and reroll_hits:
        hit_roll = random.randint(1, 6)

    hit_success = hit_roll >= hit_value
    extra_hit = hit_roll == 6 and combo_strike and hit_success

    return hit_success, extra_hit


def roll_for_wound(wound_value, reroll_wounds):
    wound_roll = random.randint(1, 6)

    if wound_roll < wound_value and reroll_wounds:
        wound_roll = random.randint(1, 6)

    wound_success = wound_roll >= wound_value

    return wound_success


def roll_for_armor(armor_value):
    armor_roll = random.randint(1, 6)

    protected_fail = armor_roll < armor_value

    return protected_fail


def roll_for_damage(damage_value, pain_value):
    if 'D' in str(damage_value):
        damage_result = process_dice_input(damage_value)
    else:
        damage_result = int(damage_value)

    if pain_value == 7:  # 不触发pain检测
        damage = damage_result
    else:  # 进行pain检测
        damage = 0
        for _ in range(damage_result):  # check for not pain
            pain_roll = random.randint(1, 6)
            if pain_roll < pain_value:
                damage += 1

    return damage


def roll_dice(hit_value, wound_value, armor_value, damage_value, pain_value, reroll_hits, reroll_wounds, reroll_hit1,
              combo_strike):
    hit_success, extra_hit = roll_for_hit(hit_value, reroll_hits, reroll_hit1, combo_strike)

    wound_success = roll_for_wound(wound_value, reroll_wounds) if hit_success else False

    protected_fail = roll_for_armor(armor_value) if wound_success else False

    damage = roll_for_damage(damage_value, pain_value) if protected_fail else 0

    return hit_success, wound_success, protected_fail, damage, extra_hit



