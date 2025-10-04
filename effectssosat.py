from enum import Enum
class EffectType(Enum):
    YAD = "яд"
    SHIT = "щит"
    REGEN = "хилл"
    SILA_RASTET = "усиление силы"

class Effect:
    def __init__(self, name: str, effect_type: EffectType, value: int = 0):
        self.name = name
        self.effect_type = effect_type
        self.value = value

    def apply_effect(self, target: 'Human') -> str:
        if self.effect_type == EffectType.SHIT:
            return f"{target.name} получает {self.value} щита"
        elif self.effect_type == EffectType.SILA_RASTET:
            target._sila += self.value
            return f"{target.name} получает +{self.value} к силе"
        elif self.effect_type == EffectType.REGEN:
            heal = self.value
            target_hp = min(target._hp + heal, target._hpmax)
            return f"{target.name} восстаналивает {target_hp} HP"
        elif self.effect_type == EffectType.YAD:
            damage = self.value
            target.take_damage(damage)
            return f"{target.name} получает {damage} урона от Yadа"
        return ""

