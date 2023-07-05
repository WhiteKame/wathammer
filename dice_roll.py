import random
from dice_input import process_dice_input, process_input_value


def roll_for_hit(hit_value, hit_modify, reroll_hits, reroll_hit1, combo_strike, lethal_hits):
    hit_roll = random.randint(1, 6)

    # 暴击命中
    critical_hit = 6
    lethal_hits_success = False

    if hit_roll == critical_hit and lethal_hits:
        lethal_hits_success = True

    # Check for extra hit before applying hit modify
    if hit_roll == 6 and combo_strike != 0:
        if combo_strike == 'D3':
            extra_hit = random.randint(1, 3)
        else:
            extra_hit = combo_strike
    else:
        extra_hit = 0

    if hit_roll == 1 and reroll_hit1:
        hit_roll = random.randint(1, 6)
    elif hit_roll < hit_value and reroll_hits:
        hit_roll = random.randint(1, 6)

    # Apply hit modify after checking for extra hit
    hit_roll_modified = hit_roll + hit_modify

    # If unmodified roll is 6, hit is always successful. If unmodified roll is 1, hit always fails
    if hit_roll == 6:
        hit_success = True
    elif hit_roll == 1:
        hit_success = False
    else:
        hit_success = hit_roll_modified >= hit_value

    return hit_success, extra_hit, lethal_hits_success


def roll_for_wound(wound_value, wound_modify, reroll_wounds, mortal_wound, anti):
    wound_roll = random.randint(1, 6)

    # 暴击造伤
    anti = int(anti)

    # 如果 wound_roll 大于等于 anti，设定暴击伤害和造伤成功
    if wound_roll >= anti:
        mortal_wound_success = True
        wound_success = True
    else:
        # 否则按照原来的逻辑判断
        if wound_roll == 6 and mortal_wound:
            mortal_wound_success = True
        else:
            mortal_wound_success = False

        # 造伤修正
        wound_roll_modified = wound_roll + wound_modify

        if wound_roll < wound_value and reroll_wounds:
            wound_roll = random.randint(1, 6)

        # 未修正的6永远成功，未修正的1永远失败
        if wound_roll == 6:
            wound_success = True
        elif wound_roll == 1:
            wound_success = False
        else:
            wound_success = wound_roll_modified >= wound_value

    return wound_success, mortal_wound_success


def roll_for_armor(armor_value, armor_modify):
    armor_roll = random.randint(1, 6)
    armor_roll_modified = armor_roll - armor_modify

    if armor_roll == 1:
        protected_fail = False
    else:
        protected_fail = armor_roll_modified < armor_value

    return protected_fail


def roll_for_damage(damage_value, pain_value):
    # print(f"damage_value = {damage_value}, pain_value = {pain_value}")  # 添加打印语句
    # 当'伤害值'包含'D'时，假定它表示骰子的投掷
    if 'D' in str(damage_value):
        damage_result = process_dice_input(damage_value)
    else:
        damage_result = int(damage_value)
    # print(f"damage_result = {damage_result}")  # 添加打印语句

    damage = 0
    # 如果'不怕疼'值为7，则无需进行'不怕疼'检测，直接返回伤害结果
    if pain_value == 7:
        damage = damage_result
    else:
        for _ in range(damage_result):  # 对每一点伤害进行'不怕疼'检测
            pain_roll = random.randint(1, 6)
            if pain_roll < pain_value:
                damage += 1
    # print(f"final damage = {damage}")  # 添加打印语句
    return damage


def roll_dice(params):
    hit_success, extra_hit, lethal_hits_success = roll_for_hit(params.hit_value, params.hit_modify, params.reroll_hits,
                                                               params.reroll_hit1,
                                                               params.combo_strike, params.lethal_hits)
    if lethal_hits_success:
        wound_success = True
        mortal_wound_success = False  # 判定致命一击
    else:
        wound_success, mortal_wound_success = roll_for_wound(params.wound_value, params.wound_modify,
                                                             params.reroll_wounds,
                                                             params.mortal_wound, params.anti) if hit_success else (
            False, False)

    # 检查是否发生了毁灭伤害，如果是，则跳过保护检查
    if mortal_wound_success:
        protected_fail = True
    else:
        protected_fail = roll_for_armor(params.armor_value, params.armor_modify) if wound_success else False

    damage = roll_for_damage(params.damage_value, params.pain_value) if protected_fail else 0
    return hit_success, wound_success, protected_fail, damage, extra_hit, mortal_wound_success
