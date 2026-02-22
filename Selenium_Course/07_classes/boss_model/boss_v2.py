# from boss import Boss_Phase2
# from .boss import Boss_Phase2
from boss import Boss

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
    
boss_phase2 = Boss_Phase2("Dragon", 150, 700, 150, 50)
print(f"Boss2 的名字是 {boss_phase2.boss_name_phase2()}")
print(f"攻擊力 : {boss_phase2.boss_attack_phase2()}")
print(f"血量 : {boss_phase2.boss_hp_phase2()}")
print(f"防禦 : {boss_phase2.boss_defense_phase2()}")
print(f"速度 : {boss_phase2.boss_speed_phase2()}")