class DiceParameters:
    def __init__(self,
                 # 攻击属性
                 hit_value, wound_value, armor_value, damage_value, pain_value,
                 # 攻击修正
                 hit_modify, wound_modify, armor_modify,
                 # 特殊规则
                 reroll_hits, reroll_wounds, reroll_hit1,
                 # 武器规则
                 combo_strike, mortal_wound,
                 attack_input=None):
        self.hit_value = hit_value
        self.wound_value = wound_value
        self.armor_value = armor_value
        self.damage_value = damage_value
        self.pain_value = pain_value
        self.hit_modify = hit_modify
        self.wound_modify = wound_modify
        self.armor_modify = armor_modify
        self.reroll_hits = reroll_hits
        self.reroll_wounds = reroll_wounds
        self.reroll_hit1 = reroll_hit1
        self.combo_strike = combo_strike
        self.mortal_wound = mortal_wound
        self.attack_input = attack_input
