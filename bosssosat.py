import random
from enum import Enum

class Human:
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self._hp = 100
        self._hpmax = 100
        self._mp = 100
        self._mpmax = 100
        self._level = level
        self._sila = 10
        self._lovkost = 5
        self._um = 5

    @property
    def  name(self) -> str:
        return self.name

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    def iniciativa(self) -> int:
        return self._lovkost + random.randint(1,5)

    def poluchit_uron(self, damage: int) -> int:
        actual_damage = damage

        shit_effects = [e for e in self._effects if e.effect_tupe == EffectType.SHIT]
        for effect in shit_effects:
            if effect.value >= damage:
                effect.value -= damage
                damage = 0
                if effect.value <= 0:
                    self._effects.remove(effect)
                break
            else:
                damage -= effect.value
                self._effects.remove(effect)

        self._hp = max(0, self._hp - damage)
        return damage

    def ataka(self, target: 'Human') -> str:
        if not self.is_alive:
            return f"{self.name} умер, не может атака делат"

        base_damage = self._sila
        actual_damage = target.poluchit_uron(base_damage)
        return f"{self.name} атакует {target.name} и дэлаит стока {actual_damage} урона"

    @property
    def hp_ystalost(self)-> float:
        return self._hp / self._hpmax



