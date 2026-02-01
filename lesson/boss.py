# TODO(2/2): 寫兩層繼承範例 (可使用AI並解析), 有空可以拆成多個檔案試試看
# 我想做一個遊戲的 BOSS 有名稱，攻擊力，有血量，有防禦，有速度
class Boss:
    def __init__(self , name, attack, hp, defense, speed):
        self.name = name
        self.attack = attack
        self.hp = hp
        self.defense = defense
        self.speed = speed
    def boss_name (self):
        return self.name
    def boss_attack(self):
        return self.attack
    def boss_hp(self):
        return self.hp
    def boss_defense(self):
        return self.defense
    def boss_speed(self):
        return self.speed
    def __repr__(self):
        return f"Boss('{self.name}', {self.attack}, {self.hp}, {self.defense}, {self.speed})"
    
class Boss_Phase2(Boss):
    def __init__(self, name_phase2, attack_phase2, hp_phase2, defense_phase2, speed_phase2):
        super().__init__(name_phase2, attack_phase2, hp_phase2, defense_phase2, speed_phase2)
    def boss_name_phase2(self):
        return "Super" + self.name
    def boss_attack_phase2(self):
        return self.attack + 50
    def boss_hp_phase2(self):
        return self.hp + 200
    def boss_defense_phase2(self):
        return self.defense + 100   
    def boss_speed_phase2(self):
        return self.speed + 20
        