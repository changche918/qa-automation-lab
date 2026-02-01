# TODO(2/2): 寫兩層繼承範例 (可使用AI並解析), 有空可以拆成多個檔案試試看
# 做一個遊戲的 BOSS 有攻擊力  有血量 有防禦 有速度
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
