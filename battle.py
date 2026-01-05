import random

from user import User

class BattleClasses:
    class Character:
        def __init__(self, name: str, char_class: str):
            self.name = name
            self.class_name = char_class
            self.hp = 100
            self.max_hp = 100

            if char_class == "warrior":
                self.attack = 15
                self.defense = 10
            elif char_class == "mage":
                self.attack = 20
                self.defense = 5
            elif char_class == "archer":
                self.attack = 18
                self.defense = 7
            else:
                self.attack = 12
                self.defense = 3

        def take_damage(self, damage: int) -> int:
            actual_damage = max(1, damage - self.defense)
            self.hp -= actual_damage
            if self.hp < 0:
                self.hp = 0
            return actual_damage

        @property
        def is_alive(self):
            return self.hp > 0

    @staticmethod
    def play(user: User) -> bool:
        print("\nБИТВА С БОМЖОМ ВИТАЛЕЙ")
        print("-" * 30)
        print("Виталий: 'А ну иди сюда, студентик!'")

        print("\nВыберите класс для битвы:")
        print("1. Воин (атака: 15, защита: 10)")
        print("2. Маг (атака: 20, защита: 5)")
        print("3. Лучник (атака: 18, защита: 7)")

        while True:
            try:
                choice = int(input("Ваш выбор (1-3): "))
                if 1 <= choice <= 3:
                    classes = ["warrior", "mage", "archer"]
                    player_class = classes[choice - 1]
                    break
                else:
                    print("Неверный выбор!")
            except ValueError:
                print("Введите число!")

        player = BattleClasses.Character(user.username, player_class)
        enemy = BattleClasses.Character("Бомж Виталий", "hobo")

        round_num = 1

        while player.is_alive and enemy.is_alive:
            print(f"\nРАУНД {round_num}")
            print(f"{player.name}: {player.hp}/{player.max_hp} HP")
            print(f"{enemy.name}: {enemy.hp}/{enemy.max_hp} HP")

            print(f"\nВаш ход!")
            damage = random.randint(player.attack - 5, player.attack + 5)
            actual_damage = enemy.take_damage(damage)
            print(f"Вы нанесли {actual_damage} урона Виталию!")

            if not enemy.is_alive:
                break

            print(f"\nХод Виталия!")
            damage = random.randint(enemy.attack - 3, enemy.attack + 3)
            actual_damage = player.take_damage(damage)
            print(f"Виталий нанес вам {actual_damage} урона!")

            round_num += 1
            input("\nНажмите Enter для продолжения...")

        if player.is_alive:
            print(f"\nВЫ ПОБЕДИЛИ! Виталий повержен!")
            user.hp = player.hp
            user.quests_completed["vitaly_battle"] = True
            return True
        else:
            print(f"\nВЫ ПРОИГРАЛИ! Виталий оказался сильнее...")
            user.hp = 0
            return False

