from boss import Boss

boss1 = Boss("Dragon", 100, 500, 50, 30)
print(f"Boss1 的名字是 {boss1.boss_name()}")
print(f"攻擊力 : {boss1.boss_attack()}")
print(f"血量 : {boss1.boss_hp()}")
print(f"防禦 : {boss1.boss_defense()}")
print(f"速度 : {boss1.boss_speed()}")