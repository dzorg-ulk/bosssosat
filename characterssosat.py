class Warrior(Human):
    def init(self, name: str):
        super().init(name)
        self._hpmax = 150
        self._hp = 150
        self._sila = 15
        self._lovkost = 8
        self._um = 5
    
    def attack(self, target: 'Human') -> str:
        if not self.is_alive:
            return f"{self.name} не может атаковать, так как мёртв!"
        
        else
          actual_damage = target.take_damage(base_damage)
          return f"{self.name} атакует {target.name} и наносит {actual_damage} урона"
    
    def special_skill(self, targets: List['Human']) -> str:
        """Разрубающий удар - атака по всем целям"""
        if self._mp < 20:
            return f"Недостаточно MP для использования Разрубающего удара!"
        
        self._mp -= 20
        results = [f"{self.name} использует Разрубающий удар!"] 
        
        for target in targets:
            if target.is_alive:
                damage = self._strength // 2
                actual_damage = target.take_damage(damage)
                results.append(f"Наносит {actual_damage} урона {target.name}")
        
        return " ".join(results)

class Mage(Human):
    def init(self, name: str):
        super().init(name)
        self._hpmax = 80
        self._hp = 80
        self._mpmax = 100
        self._mp = 100
        self._sila = 5
        self._lovkost = 8
        self._um = 18
    
    def attack(self, target: 'Human') -> str:
        """Маг атакует магией"""
        if not self.is_alive:
            return f"{self.name} не может атаковать, так как мёртв!"
        
        base_damage = self._um // 2
        actual_damage = target.take_damage(base_damage)
        
        return f"{self.name} бросает магический снаряд в {target.name} и наносит {actual_damage} урона"
    
    def special_skill(self, targets: List['Human']) -> str:
        """Огненный шар - мощная атака по одной цели с поджогом"""
        if self._mp < 30:
            return f"Недостаточно MP для использования Огненного шара!"
        
        if not targets:
            return "Нет целей для атаки!"
        
        self._mp -= 30
        target = targets[0]
        
        if not target.is_alive:
            return "Цель мертва!"
        
        base_damage = self._um
        actual_damage = target.take_damage(base_damage)
        
        yad_effect = Effect("Горение", EffectType.YAD, 3, 5)
        target.add_effect(yad_effect)
        
        return (f"{self.name} запускает Огненный шар в {target.name}! "
                f"Наносит {actual_damage} урона и поджигает цель")

class Healer(Human):
    def init(self, name: str):
        super().init(name)
        self._hpmax = 90
        self._hp = 90
        self._mpmax = 80
        self._mp = 80
        self._sila = 6
        self._lovkost = 10
        self._um = 15
    
    def attack(self, target: 'Human') -> str:
        """Лекарь атакует посохом"""
        if not self.is_alive:
            return f"{self.name} не может атаковать, так как мёртв!"
        
        base_damage = max(self._sila, self._um // 3)
        actual_damage = target.take_damage(base_damage)
        
        return f"{self.name} бьёт посохом {target.name} и наносит {actual_damage} урона"
    
    def special_skill(self, targets: List['Human']) -> str:
        """Исцеление - восстанавливает HP союзникам"""
        if self._mp < 25:
            return f"Недостаточно MP для использования Исцеления!"
        
        if not targets:
            return "Нет целей для исцеления!"
        
        self._mp -= 25
        target = targets[0]
        
        if not target.is_alive:
            return "Нельзя исцелить мёртвого!"
        
        heal_amount = self._um
        old_hp = target._hp
        target._hp = min(target._hp + heal_amount, target._max_hp)
        actual_heal = target._hp - old_hp
        
        return f"{self.name} исцеляет {target.name} на {actual_heal} HP"


class Boss(Human):
    def init(self, name: str, level: int = 5):
        super().init(name, level)
        self._hpmax = 400
        self._hp = 400
        self._mpmax = 200
        self._mp = 200
        self._sila = 20
        self._lovkost = 12
        self._um = 15
        
    
    def attack(self, target: 'Human') -> str:
        """Атака босса с повышенным уроном"""
        base_damage = self._sila + 5
        actual_damage = target.take_damage(base_damage)
        return f"{self.name} мощно атакует {target.name} и наносит {actual_damage} урона!"
