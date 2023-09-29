import random

from dice_input import process_dice_input


def roll_for_hit(hit_value, hit_modify, torrent, reroll_hits, reroll_hit1, combo_strike, lethal_hits,
                 critical_hit_value, reroll_hits_failed):
    if torrent:
        hit_success = True
        extra_hit = False
        lethal_hits_success = False
    else:
        hit_roll = random.randint(1, 6)

        # 暴击命中
        critical_hit = 6
        if critical_hit_value <= critical_hit:
            critical_hit = critical_hit_value

        # 重投
        if hit_roll == 1 and reroll_hit1:
            hit_roll = random.randint(1, 6)
        elif hit_roll < hit_value and reroll_hits:
            hit_roll = random.randint(1, 6)
        elif hit_roll < critical_hit and reroll_hits_failed:
            hit_roll = random.randint(1, 6)

        # 致命一击
        lethal_hits_success = False
        if hit_roll >= critical_hit and lethal_hits:
            lethal_hits_success = True

        # 连击
        if hit_roll >= critical_hit and combo_strike != 0:
            if combo_strike == 'D3':
                extra_hit = random.randint(1, 3)
            else:
                extra_hit = int(combo_strike)
        else:
            extra_hit = 0

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


def roll_for_wound(wound_value, wound_modify, reroll_wounds, reroll_wounds1, mortal_wound, anti,
                   critical_wound_value, reroll_wounds_failed):
    wound_roll = random.randint(1, 6)

    # 暴击造伤
    anti = int(anti)
    if anti > critical_wound_value:
        anti = critical_wound_value

    if wound_roll == 1 and reroll_wounds1:
        wound_roll = random.randint(1, 6)
    elif wound_roll < wound_value and reroll_wounds:
        wound_roll = random.randint(1, 6)
    elif wound_roll < critical_wound_value and reroll_wounds_failed:
        wound_roll = random.randint(1, 6)

    # 如果 wound_roll 大于等于 anti，设定暴击伤害和造伤成功
    if wound_roll >= anti:
        wound_success = True
        # 只有在有 mortal_wound 的情况下，才将 wound_roll >= anti 的情况视为致命伤
        mortal_wound_success = mortal_wound
    else:
        # 否则按照原来的逻辑判断
        # if wound_roll >= critical_wound_value and mortal_wound:
        #     mortal_wound_success = True
        # else:
        mortal_wound_success = False

        # 造伤修正
        wound_roll_modified = wound_roll + wound_modify

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
        protected_fail = armor_roll_modified <= armor_value

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
    hit_success, extra_hit, lethal_hits_success = roll_for_hit(params.hit_value, params.hit_modify, params.torrent,
                                                               params.reroll_hits, params.reroll_hit1,
                                                               params.combo_strike, params.lethal_hits,
                                                               params.critical_hit_value, params.reroll_hits_failed)

    if lethal_hits_success:
        wound_success = True
        mortal_wound_success = False  # 判定致命一击
    else:
        wound_success, mortal_wound_success = roll_for_wound(params.wound_value, params.wound_modify,
                                                             params.reroll_wounds, params.reroll_hit1,
                                                             params.mortal_wound, params.anti,
                                                             params.critical_wound_value, params.reroll_wounds_failed) if hit_success else (
            False, False)

    # 检查是否发生了毁灭伤害，如果是，则跳过保护检查
    if mortal_wound_success:
        # 在这里增加一次“不怕疼”检测
        damage_mortal = roll_for_damage(params.damage_value, params.pain_value)
        damage = damage_mortal
        protected_fail = False

    else:
        protected_fail = roll_for_armor(params.armor_value, params.armor_modify) if wound_success else False
        damage = roll_for_damage(params.damage_value, params.pain_value) if protected_fail else 0

    return hit_success, wound_success, protected_fail, damage, extra_hit, mortal_wound_success
