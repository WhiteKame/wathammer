class DiceParameters:
    def __init__(self,
                 # 攻击属性
                 hit_value, wound_value, armor_value, damage_value, pain_value,
                 # 攻击修正
                 hit_modify, wound_modify, armor_modify,
                 # 通用规则
                 torrent, reroll_hits, reroll_wounds, reroll_hit1, reroll_wound1,
                 # 武器规则
                 combo_strike, mortal_wound, lethal_hits, anti,
                 # 特殊规则
                 reroll_hits_failed, reroll_wounds_failed,
                 # 暴击修正
                 critical_hit_value, critical_wound_value,
                 attack_input=None):
        self.hit_value = hit_value
        self.wound_value = wound_value
        self.armor_value = armor_value
        self.damage_value = damage_value
        self.pain_value = pain_value
        self.hit_modify = hit_modify
        self.wound_modify = wound_modify
        self.armor_modify = armor_modify
        self.torrent = torrent
        self.reroll_hits = reroll_hits
        self.reroll_wounds = reroll_wounds
        self.reroll_hit1 = reroll_hit1
        self.reroll_wound1 = reroll_wound1
        self.combo_strike = combo_strike
        self.mortal_wound = mortal_wound
        self.lethal_hits = lethal_hits
        self.anti = anti
        self.attack_input = attack_input
        self.reroll_hits_failed = reroll_hits_failed
        self.reroll_wounds_failed = reroll_wounds_failed
        self.critical_hit_value = critical_hit_value
        self.critical_wound_value = critical_wound_value
