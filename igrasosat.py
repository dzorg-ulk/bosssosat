class Game:
    def init(self):
        self.party: List[Human] = []
        self.boss: Optional[Boss] = None
        self.turn_count = 0
    
    def nastroyka_game(self):
        print("🎮 Добро пожаловать в мини-игру 'Пати против Босса'!")
        print("Создайте свою команду из 3 героев:")
        
        hero_classes = {
            '1': ('Воин', Warrior),
            '2': ('Маг', Mage),
            '3': ('Лекарь', Healer)
        }
        
        for i in range(3):
            print(f"\nСоздание героя #{i + 1}:")
            print("1 - Воин (много HP, сильные атаки)")
            print("2 - Маг (много MP, магические атаки)")  
            print("3 - Лекарь (исцеление, поддержка)")
            
            while True:
                choice = input("Выберите класс (1-3): ").strip()
                if choice in hero_classes:
                    class_name, class_obj = hero_classes[choice]
                    name = input(f"Введите имя для {class_name}: ").strip()
                    hero = class_obj(name)
                    self.party.append(hero)
                    print(f"✅ Создан {class_name}: {name}")
                    break
                else:
                    print("❌ Неверный выбор. Попробуйте снова.")
        
        self.boss = Boss("Дракон Разрушитель", 5)
        print(f"\n⚡ Босс создан: {self.boss.name}")
    
    def raschet_iniciativa(self) -> List[Human]:
        all_combatants = self.party + [self.boss]
        alive_combatants = [c for c in all_combatants if c.is_alive]
        return sorted(alive_combatants, key=lambda x: x.iniciativa, reverse=True)
    
    def party_is_alive(self) -> bool:
        return any(hero.is_alive for hero in self.party)
    
    def display_status(self):
        print(f"\n{'='*50}")
        print(f"Ход #{self.turn_count}")
        print(f"{'='*50}")
        
        print("👥 Ваша команда:")
        for i, hero in enumerate(self.party, 1):
            status = "💀 МЕРТВ" if not hero.is_alive else "❤️ ЖИВ"
            print(f"  {i}. {hero} [{status}]")
        
        boss_status = "💀 МЕРТВ" if not self.boss.is_alive else "❤️ ЖИВ"
        print(f"\n👹 Босс: {self.boss} [{boss_status}]")
        print(f"{'='*50}")
    
    def player_turn(self, hero: Human) -> str:
        print(f"\n🎯 Ход {hero.name}:")
        print("1 - Обычная атака")
        print("2 - Особый навык")
        print("3 - Использовать предмет")
        
        alive_targets = [t for t in [self.boss] + self.party if t.is_alive and t != hero]
        
        while True:
            choice = input("Выберите действие (1-2): ").strip()
            
            if choice == "1":
                print("Цели для атаки:")
                for i, target in enumerate(alive_targets, 1):
                    print(f"  {i} - {target.name}")
                
                try:
                    target_idx = int(input("Выберите цель: ")) - 1
                    if 0 <= target_idx < len(alive_targets):
                        return hero.attack(alive_targets[target_idx])
                    else:
                        print("❌ Неверный выбор цели")
                except ValueError:
                    print("❌ Введите число")
            
            elif choice == "2":
                if isinstance(hero, Healer):
                    heal_targets = [t for t in self.party if t.is_alive]
                    print("Цели для исцеления:")
                    for i, target in enumerate(heal_targets, 1):
                        print(f"  {i} - {target.name}")
                    
                    try:
                        target_idx = int(input("Выберите цель: ")) - 1
                        if 0 <= target_idx < len(heal_targets):
                            return hero.special_skill([heal_targets[target_idx]])
                        else:
                            print("❌ Неверный выбор цели")
                    except ValueError:
                        print("❌ Введите число")
                else:
                    return hero.special_skill([self.boss])
    
    def run_game(self): #запускsosat
        self.setup_game()
        
        while self.party_is_alive() and self.boss.is_alive:
            self.turn_count += 1
            self.display_status()
            
            turn_order = self.calculate_iniciativa()
            
            for combatant in turn_order:
                if not combatant.is_alive:
                    continue
                
                effect_result = combatant.process_effects()
                if effect_result:
                    print(f"📢 {effect_result}")
                
                if not combatant.is_alive:
                    continue
                
                if combatant == self.boss:
                    print(f"\n👹 Ход {self.boss.name}:")
                    result = self.boss.special_skill(self.party)
                    print(f"  {result}")
                
                elif combatant in self.party:
                    result = self.player_turn(combatant)
                    print(f"  {result}")
                
                if not self.boss.is_alive or not self.party_is_alive():
                    break
            
            input("\n⏎ Нажмите Enter для продолжения...")
        
        print(f"\n{'='*50}")
        if not self.boss.is_alive:
            print("🎉 ПОБЕДА! Ваша команда победила босса!")
        else:
            print("💀 ПОРАЖЕНИЕ! Босс уничтожил вашу команду.")
        print(f"{'='*50}")


if name == "main":
    game = Game()
    game.run_game()

