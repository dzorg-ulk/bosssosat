import json
import os
import random
import hashlib
import time
from typing import Dict, List, Optional, Any
import sys


class User:
    def __init__(self, username: str):
        self.username = username
        self.password_hash = ""
        self.artifacts: List[str] = []
        self.achievements: List[str] = []
        self.hp = 100
        self.max_hp = 100
        self.location = "start"
        self.story_progress = 0
        self.father_respect = 0
        self.drunk_level = 0
        self.quests_completed = {
            "parents": False,
            "friends": False,
            "father_jokes": False,
            "vitaly_battle": False,
            "rps_game": False,
            "baba_zina": False
        }

    def to_dict(self) -> Dict:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "artifacts": self.artifacts,
            "achievements": self.achievements,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "location": self.location,
            "story_progress": self.story_progress,
            "father_respect": self.father_respect,
            "drunk_level": self.drunk_level,
            "quests_completed": self.quests_completed
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        user = cls(data["username"])
        user.password_hash = data["password_hash"]
        user.artifacts = data["artifacts"]
        user.achievements = data["achievements"]
        user.hp = data["hp"]
        user.max_hp = data["max_hp"]
        user.location = data["location"]
        user.story_progress = data["story_progress"]
        user.father_respect = data["father_respect"]
        user.drunk_level = data["drunk_level"]
        user.quests_completed = data.get("quests_completed", {
            "parents": False, "friends": False, "father_jokes": False,
            "vitaly_battle": False, "rps_game": False, "baba_zina": False
        })
        return user

    def check_all_quests_completed(self) -> bool:
        return all(self.quests_completed.values())


class AuthSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.current_user: Optional[User] = None

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str) -> bool:
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}

        if username in users:
            return False

        user = User(username)
        user.password_hash = self.hash_password(password)

        users[username] = user.to_dict()

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

        self.current_user = user
        return True

    def login(self, username: str, password: str) -> bool:
        if not os.path.exists(self.users_file):
            return False

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        if username not in users:
            return False

        if users[username]["password_hash"] != self.hash_password(password):
            return False

        self.current_user = User.from_dict(users[username])
        return True

    def save_user(self):
        if not self.current_user:
            return

        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}

        users[self.current_user.username] = self.current_user.to_dict()

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def save_game(self, save_name: str = "quicksave"):
        if not self.current_user:
            return False

        save_data = {
            "user": self.current_user.to_dict(),
            "timestamp": time.time()
        }

        save_dir = "saves"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        save_file = os.path.join(save_dir, f"{save_name}.json")

        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=2)

        print(f"Игра сохранена: {save_name}")
        return True

    def load_game(self, save_name: str = "quicksave") -> bool:
        save_file = os.path.join("saves", f"{save_name}.json")

        if not os.path.exists(save_file):
            return False

        with open(save_file, 'r') as f:
            save_data = json.load(f)

        self.current_user = User.from_dict(save_data["user"])
        print(f"Загружено сохранение: {save_name}")
        return True


class RockPaperScissors:
    @staticmethod
    def play() -> str:
        choices = ["камень", "ножницы", "бумага"]
        win_rules = {
            "камень": "ножницы",
            "ножницы": "бумага",
            "бумага": "камень"
        }

        print("\nИГРА: КАМЕНЬ-НОЖНИЦЫ-БУМАГА")
        print("-" * 30)

        while True:
            print("\nВыберите: 1-камень, 2-ножницы, 3-бумага")
            try:
                player_choice = int(input("Ваш выбор (1-3): "))
                if 1 <= player_choice <= 3:
                    player = choices[player_choice - 1]
                    break
                else:
                    print("Неверный выбор!")
            except ValueError:
                print("Введите число!")

        computer = random.choice(choices)
        print(f"\nВы выбрали: {player}")
        print(f"Компьютер выбрал: {computer}")

        if player == computer:
            print("НИЧЬЯ!")
            return "draw"
        elif win_rules[player] == computer:
            print("ВЫ ВЫИГРАЛИ!")
            return "win"
        else:
            print("Компьютер выиграл!")
            return "lose"


class TwentyOneMatches:
    @staticmethod
    def play() -> bool:
        matches = 21

        print("\nИГРА: 21 СПИЧКА")
        print("-" * 30)
        print("Правила: берете 1, 2 или 3 спички.")
        print("Кто возьмет последнюю - проиграл!")

        player_turn = random.choice([True, False])
        if player_turn:
            print("\nВы ходите первым!")
        else:
            print("\nПротивник ходит первым!")

        while matches > 0:
            print(f"\nОсталось спичек: {matches}")
            print("[" + "| " * matches + "]")

            if player_turn:
                while True:
                    try:
                        move = int(input("Ваш ход (1-3): "))
                        if 1 <= move <= 3 and move <= matches:
                            matches -= move
                            break
                        else:
                            print("Можно взять 1-3 спички!")
                    except ValueError:
                        print("Введите число!")
            else:
                if matches == 1:
                    move = 1
                elif matches <= 4:
                    move = matches - 1
                else:
                    move = random.randint(1, 3)
                    move = min(move, matches)

                print(f"Противник берет {move} спичку(и)")
                matches -= move

            if matches == 0:
                if player_turn:
                    print("\nВы взяли последнюю спичку и ПРОИГРАЛИ!")
                    return False
                else:
                    print("\nПротивник взял последнюю спичку! ВЫ ВЫИГРАЛИ!")
                    return True

            player_turn = not player_turn

        return False


class FatherJokes:
    jokes = [
        {
            "setup": "Этой ночью я пил с русскими. Всю ночь они рассказывали анекдоты и доказывали мне, что Россия, это страна дураков и плохих дорог. Под утро я с ними согласился, и они набили мне...",
            "answer": ["морду", "физиономию", "рожу"]
        },
        {
            "setup": "Блин! - сказал слон, наступив на...",
            "answer": ["колобка", "колобок"]
        },
        {
            "setup": "Как сказать по татарски вперед? - спрашивает русский у татарина. - Алга! - говорит татарин. - А как сказать назад? - У татар нет назад, они разворачиваются и...",
            "answer": ["алга", "опять алга"]
        },
        {
            "setup": "Я согрешил батюшка! - И в чем же ты грешен? - Я обманул еврея! - Успокойся, это не грех, а...",
            "answer": ["чудо", "настоящее чудо"]
        }
    ]

    @staticmethod
    def play(user: User) -> bool:
        print("\nОТЕЦ: 'Ну что, сынок, проверю твое чувство юмора!'")
        print("Закончи мои любимые анекдоты...")

        random.shuffle(FatherJokes.jokes)
        jokes_to_play = FatherJokes.jokes[:3]
        correct_answers = 0

        for i, joke in enumerate(jokes_to_play):
            print(f"\nАнекдот {i + 1} из {len(jokes_to_play)}")
            print(f"\nОтец: '{joke['setup']}'")

            answer = input("\nТвой ответ: ").strip().lower()

            is_correct = any(correct_answer in answer for correct_answer in joke["answer"])

            if is_correct:
                print("Отец: 'Ха-ха! Правильно! Молодец!'")
                correct_answers += 1
                user.father_respect += 10
            else:
                correct_variant = joke["answer"][0]
                print(f"Отец: 'Эх... Правильно было бы: {correct_variant}'")
                user.hp -= 5

        success_rate = correct_answers / len(jokes_to_play)

        print(f"\nРЕЗУЛЬТАТЫ:")
        print(f"Правильных ответов: {correct_answers}/{len(jokes_to_play)}")

        if success_rate >= 0.7:
            print("Отец: 'Ну ты даешь! Горжусь тобой, сынок!'")
            user.artifacts.append("Уважение отца")
            user.achievements.append("Настоящий сын")
            user.father_respect += 50
            user.quests_completed["father_jokes"] = True
            return True
        elif success_rate >= 0.4:
            print("Отец: 'Ну... сойдет. Но могло быть и лучше.'")
            user.father_respect += 20
            user.quests_completed["father_jokes"] = True
            return True
        else:
            print("Отец: 'Да, испортила тебя Москва...'")
            user.hp -= 10
            return False


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


class StudentGame:
    def __init__(self):
        self.auth = AuthSystem()
        self.user: Optional[User] = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print("=" * 60)
        print("           СТУДЕНТ: ВОЗВРАЩЕНИЕ В РОДНОЙ ГОРОД")
        print("=" * 60)

    def add_artifact(self, artifact: str):
        if self.user and artifact not in self.user.artifacts:
            self.user.artifacts.append(artifact)
            print(f"\nВы получили артефакт: {artifact}")

    def add_achievement(self, achievement: str):
        if self.user and achievement not in self.user.achievements:
            self.user.achievements.append(achievement)
            print(f"\nВы получили достижение: {achievement}")

    def show_status(self):
        if not self.user:
            return

        print(f"\nСТАТУС:")
        print(f"Игрок: {self.user.username}")
        print(f"❤️  Здоровье: {self.user.hp}/{self.user.max_hp}")
        print(f"Уважение отца: {self.user.father_respect}")
        print(f"Уровень опьянения: {self.user.drunk_level}/100")

        completed_quests = sum(1 for q in self.user.quests_completed.values() if q)
        total_quests = len(self.user.quests_completed)
        print(f"Квестов выполнено: {completed_quests}/{total_quests}")

        if self.user.artifacts:
            print(f"\nАртефакты ({len(self.user.artifacts)}):")
            for art in self.user.artifacts:
                print(f"  • {art}")

        if self.user.achievements:
            print(f"\nДостижения ({len(self.user.achievements)}):")
            for ach in self.user.achievements:
                print(f"  • {ach}")

    def show_final_results(self):
        self.print_header()
        print("\n" + "=" * 60)
        print("                 ИГРА ЗАВЕРШЕНА!")
        print("=" * 60)

        print(f"\nПОЗДРАВЛЯЕМ, {self.user.username}!")
        print("Вы завершили все квесты в родном городе!")

        print("\n" + "=" * 60)
        print("ВАШИ РЕЗУЛЬТАТЫ:")
        print("=" * 60)

        print(f"\nФИНАЛЬНЫЙ СТАТУС:")
        print(f"Здоровье: {self.user.hp}/{self.user.max_hp}")
        print(f"Уважение отца: {self.user.father_respect}")
        print(f"Уровень опьянения: {self.user.drunk_level}/100")

        completed_quests = sum(1 for q in self.user.quests_completed.values() if q)
        total_quests = len(self.user.quests_completed)
        print(f"Квестов выполнено: {completed_quests}/{total_quests}")

        if self.user.artifacts:
            print(f"\nСОБРАННЫЕ АРТЕФАКТЫ ({len(self.user.artifacts)}):")
            for i, art in enumerate(self.user.artifacts, 1):
                print(f"{i}. {art}")

        if self.user.achievements:
            print(f"\nПОЛУЧЕННЫЕ ДОСТИЖЕНИЯ ({len(self.user.achievements)}):")
            for i, ach in enumerate(self.user.achievements, 1):
                print(f"{i}. {ach}")

        print("\n" + "=" * 60)
        print("ОБЩИЙ ВЫВОД:")
        print("=" * 60)

        if self.user.father_respect >= 50:
            print("• Вы заслужили уважение отца")
        if self.user.drunk_level >= 50:
            print("• Вы хорошо повеселились с друзьями")
        if self.user.hp >= 80:
            print("• Вы сохранили хорошее здоровье")
        elif self.user.hp <= 30:
            print("• Вы сильно пострадали в приключениях")

        if len(self.user.artifacts) >= 3:
            print("• Вы собрали много ценных артефактов")

        print("\n" + "=" * 60)

    def auth_menu(self):
        self.print_header()
        print("\nАВТОРИЗАЦИЯ")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")

        while True:
            choice = input("\nВыберите действие (1-3): ")

            if choice == "1":
                self.register()
                break
            elif choice == "2":
                self.login()
                break
            elif choice == "3":
                print("\nДо свидания!")
                sys.exit(0)
            else:
                print("Неверный выбор!")

    def register(self):
        self.print_header()
        print("\nРЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ")

        while True:
            username = input("\nПридумайте логин: ").strip()
            if not username:
                print("Логин не может быть пустым!")
                continue

            password = input("Придумайте пароль: ").strip()
            if not password:
                print("Пароль не может быть пустым!")
                continue

            if self.auth.register(username, password):
                print(f"\nРегистрация успешна! Добро пожаловать, {username}!")
                self.user = self.auth.current_user
                break
            else:
                print("Пользователь с таким логином уже существует!")
                continue_choice = input("Попробовать снова? (да/нет): ").lower()
                if continue_choice not in ['да', 'д', 'yes', 'y']:
                    self.auth_menu()
                    return

    def login(self):
        self.print_header()
        print("\nВХОД В СИСТЕМУ")

        attempts = 3
        while attempts > 0:
            print(f"\nПопыток осталось: {attempts}")
            username = input("Логин: ").strip()
            password = input("Пароль: ").strip()

            if self.auth.login(username, password):
                print(f"\nВход успешен! Добро пожаловать, {username}!")
                self.user = self.auth.current_user

                if os.path.exists("saves/quicksave.json"):
                    load = input("\nНайдено сохранение. Загрузить? (да/нет): ").lower()
                    if load in ['да', 'д', 'yes', 'y']:
                        self.auth.load_game()
                return

            attempts -= 1
            print(f"Неверный логин или пароль! Осталось попыток: {attempts}")

        print("\nСлишком много неудачных попыток!")
        input("Нажмите Enter для возврата в меню...")
        self.auth_menu()

    def save_menu(self):
        self.print_header()
        print("\nМЕНЮ СОХРАНЕНИЯ")
        print("1. Быстрое сохранение")
        print("2. Создать новое сохранение")
        print("3. Загрузить сохранение")
        print("4. Вернуться в игру")

        while True:
            choice = input("\nВыберите действие (1-4): ")

            if choice == "1":
                self.auth.save_game()
                input("\nНажмите Enter для продолжения...")
                break
            elif choice == "2":
                save_name = input("Введите название сохранения: ").strip()
                if save_name:
                    self.auth.save_game(save_name)
                input("\nНажмите Enter для продолжения...")
                break
            elif choice == "3":
                if os.path.exists("saves"):
                    saves = [f.replace(".json", "") for f in os.listdir("saves") if f.endswith(".json")]
                    if saves:
                        print("\nДоступные сохранения:")
                        for i, save in enumerate(saves, 1):
                            print(f"{i}. {save}")

                        try:
                            save_choice = int(input("\nВыберите номер сохранения: ")) - 1
                            if 0 <= save_choice < len(saves):
                                self.auth.load_game(saves[save_choice])
                                print("Игра загружена!")
                            else:
                                print("Неверный номер!")
                        except ValueError:
                            print("Введите число!")
                    else:
                        print("Нет доступных сохранений!")
                else:
                    print("Нет доступных сохранений!")
                input("\nНажмите Enter для продолжения...")
                break
            elif choice == "4":
                break
            else:
                print("Неверный выбор!")

    def parents_path(self):
        self.print_header()
        print("\nВЫ ПРИШЛИ К РОДИТЕЛЯМ")
        print("\nМама: 'Сыночек, приехал! Садись, чайку попьем!'")
        print("Отец сидит за столом и смотрит телевизор.")

        print("\n1. Выпить чай с мамой")
        print("2. Отказаться от чая")

        while True:
            choice = input("\nВаш выбор (1-2): ")

            if choice == "1":
                print("\nВы пьете чай с мамой...")
                time.sleep(2)
                self.user.hp = min(self.user.max_hp, self.user.hp + 5)
                self.add_artifact("Использованный пакетик Greenfield")
                print("❤️  +5 HP")
                print("\nМама: 'Попей, сынок, попей...'")
                time.sleep(2)
                print("\nМама уходит мыть полы в другую комнату.")
                break
            elif choice == "2":
                print("\nВы: 'Спасибо, мам, не хочу.'")
                print("Мама: 'Ну как знаешь...'")
                break
            else:
                print("Неверный выбор!")

        input("\nНажмите Enter для продолжения...")

        self.print_header()
        print("\nОстаетесь наедине с отцом...")
        print("Отец отрывается от телевизора и смотрит на вас.")

        self.user.quests_completed["parents"] = True

        if self.user.hp > 0:
            play_jokes = input("\nОтец: 'Ну что, проверим твое чувство юмора?' (да/нет): ").lower()

            if play_jokes in ['да', 'д', 'yes', 'y']:
                result = FatherJokes.play(self.user)
                if not result:
                    print("\nОтец: 'Да, испортила тебя Москва...'")
                    print("Отец разочарованно возвращается к телевизору.")

                    go_friends = input("\nПойти проведать друзей? (да/нет): ").lower()
                    if go_friends in ['да', 'д', 'yes', 'y']:
                        self.friends_path()
                        return
                else:
                    print("\nОтец: 'Молодец, сынок! Вот это я понимаю!'")
                    self.add_artifact("Уважение отца")
            else:
                print("\nОтец: 'Ну и ладно...'")
                print("Вы чувствуете неловкость в воздухе.")

        if self.check_all_quests_completed():
            self.game_completed()
            return

        self.print_header()
        print("\nЧто делать дальше?")
        print("1. Остаться дома с родителями")
        print("2. Пойти к друзьям")

        while True:
            choice = input("\nВаш выбор (1-2): ")

            if choice == "1":
                print("\nВы решаете остаться дома.")
                print("Вечер проходит тихо за семейным ужином.")
                self.user.hp = self.user.max_hp
                self.add_achievement("Семейный вечер")
                self.end_game()
                break
            elif choice == "2":
                self.friends_path()
                break
            else:
                print("Неверный выбор!")

    def friends_path(self):
        self.print_header()
        print("\nВЫ РЕШИЛИ ПОВИДАТЬСЯ С ДРУЗЬЯМИ")
        print("\nДруг: 'Приезжай к нам на дачу, тут вся компания!'")
        print("Вы направляетесь на дачу...")
        time.sleep(2)

        print("\nПо дороге на вас нападает местный бомж Виталий!")
        print("Виталий: 'А ну, студент, дай денег на опохмел!'")

        input("\nНажмите Enter для начала битвы...")

        battle_won = BattleClasses.play(self.user)

        if not battle_won:
            print("\nВЫ ОТПРАВЛЕНЫ В ТРАВМПУНКТ")
            print("Вы проиграли бомжу Виталию и попали в больницу.")
            self.add_achievement("Предновогодний травмпункт")
            self.end_game()
            return

        print("\nВы победили Виталия и добрались до дачи!")
        print("Друзья встречают вас радостными криками!")
        self.add_artifact("Чекушка")
        self.user.drunk_level += 20

        self.user.quests_completed["friends"] = True

        print("\nДруг: 'Выглядишь потрепанно, выпей зелье здоровья!'")
        print("1. Выпить зелье (+20 HP, но временное помутнение рассудка)")
        print("2. Отказаться")

        while True:
            choice = input("\nВаш выбор (1-2): ")

            if choice == "1":
                print("\nВы выпиваете странное зелье...")
                self.user.hp = min(self.user.max_hp, self.user.hp + 20)
                self.user.drunk_level += 30
                print("❤️  +20 HP")
                print("Вы чувствуете легкое головокружение...")

                print("\nСЛЕДУЮЩИЕ 3 РЕПЛИКИ ВЫ ВИДИТЕ В ИСКАЖЕННОМ ВИДЕ:")
                time.sleep(1)

                for i in range(3):
                    random_text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=20))
                    print(f"{random_text}")
                    if i < 2:
                        input("Нажмите Enter для следующей реплики...")

                print("\nЭффект зелья прошел!")
                break
            elif choice == "2":
                print("\nВы: 'Нет, спасибо, я и так в норме.'")
                break
            else:
                print("Неверный выбор!")

        print("\nОказывается, весь алкоголь на даче почти закончился!")
        print("Друг: 'Давай сыграем в камень-ножницы-бумага за последнюю бутылку!'")

        input("\nНажмите Enter для игры...")

        rps_result = RockPaperScissors.play()

        if rps_result == "win":
            print("\nВЫ ВЫИГРАЛИ ПОСЛЕДНЮЮ БУТЫЛКУ!")
            print("Друзья: 'Ну ты везунчик!'")
            self.add_artifact("Честь")
            self.user.drunk_level += 20
            self.user.quests_completed["rps_game"] = True

            if self.check_all_quests_completed():
                self.game_completed()
                return

            self.after_party_choice()

        else:
            print("\nВЫ ПРОИГРАЛИ ПОСЛЕДНЮЮ БУТЫЛКУ!")
            print("Друг: 'Ха-ха! Иди купи еще в ларьке!'")

            self.baba_zina_path()

    def baba_zina_path(self):
        self.print_header()
        print("\nВЫ ИДЕТЕ К ЛАРЬКУ БАБЫ ЗИНЫ")
        print("\nБаба Зина: 'Чего надо, пацан?'")
        print("Вы: 'Мне бутылку пива, пожалуйста.'")
        print("Баба Зина: '50 рублей.'")

        print("\nУ вас есть только 49 рублей...")
        print("Вы: 'У меня только 49...'")
        print("Баба Зина: 'Ну так иди работай! Хотя...'")
        print("Баба Зина: 'Выиграешь у меня в 21 спичку - дам в долг!'")

        play_game = input("\nСыграть с бабой Зиной? (да/нет): ").lower()

        if play_game in ['да', 'д', 'yes', 'y']:
            won = TwentyOneMatches.play()

            if won:
                print("\nВЫ ВЫИГРАЛИ У БАБЫ ЗИНЫ!")
                print("Баба Зина: 'Ладно, бери, черт с тобой...'")
                self.add_artifact("Чирик из старой куртки")
                self.add_achievement("Уважение бывших одноклассников")
                self.user.quests_completed["baba_zina"] = True

                print("\nВы возвращаетесь на дачу с пивом!")
                print("Друзья встречают вас как героя!")
                self.user.drunk_level += 30

                if self.check_all_quests_completed():
                    self.game_completed()
                    return

                self.after_party_choice()
            else:
                print("\nВЫ ПРОИГРАЛИ БАБЕ ЗИНЕ!")
                print("Баба Зина: 'Лох! Иди отсюда!'")
                self.add_achievement("Лох")

                print("\nВы позорно возвращаетесь домой...")
                input("\nНажмите Enter для продолжения...")
                self.parents_path()
        else:
            print("\nВы: 'Не, я лучше домой пойду...'")
            self.parents_path()

    def after_party_choice(self):
        self.print_header()
        self.show_status()

        if self.check_all_quests_completed():
            self.game_completed()
            return

        if self.user.hp > self.user.max_hp // 2:
            print("\nВечер в самом разгаре...")
            print("1. Остаться на даче с друзьями")
            print("2. Пойти домой к родителям")

            while True:
                choice = input("\nВаш выбор (1-2): ")

                if choice == "1":
                    print("\nВы остаетесь с друзьями до утра!")
                    print("Это была лучшая ночь за долгое время!")
                    self.user.drunk_level = 100
                    self.add_achievement("Легенда дачи")

                    if self.check_all_quests_completed():
                        self.game_completed()
                    else:
                        self.end_game()
                    break
                elif choice == "2":
                    print("\nВы решаете пойти домой...")
                    self.parents_path()
                    break
                else:
                    print("Неверный выбор!")
        else:
            print("\nВы чувствуете себя слишком плохо, чтобы продолжать...")
            print("Вас отвезли домой.")
            self.end_game()

    def check_all_quests_completed(self) -> bool:
        if not self.user:
            return False
        return self.user.check_all_quests_completed()

    def game_completed(self):
        self.show_final_results()

        self.auth.save_game()

        print("\n" + "=" * 60)
        print("ВЫБЕРИТЕ ДАЛЬНЕЙШЕЕ ДЕЙСТВИЕ:")
        print("1. Сохраниться и выйти")
        print("2. Пройти еще раз")
        print("=" * 60)

        while True:
            choice = input("\nВаш выбор (1-2): ")

            if choice == "1":
                self.auth.save_game("final_save")
                print("\nИгра сохранена. До свидания!")
                sys.exit(0)
            elif choice == "2":
                self.start_new_game()
                break
            else:
                print("Неверный выбор!")

    def start_new_game(self):
        print("\nНачинаем новую игру...")
        time.sleep(2)

        self.user.hp = 100
        self.user.drunk_level = 0
        self.user.location = "start"
        self.user.story_progress = 0

        for key in self.user.quests_completed:
            self.user.quests_completed[key] = False

        self.auth.save_game()
        self.play()

    def end_game(self):
        self.print_header()
        print("\nИГРА ЗАВЕРШЕНА")
        print("=" * 60)

        self.show_status()

        self.auth.save_game()

        print("\n" + "=" * 60)
        print("Что дальше?")
        print("1. Начать новую игру")
        print("2. Выйти в меню")
        print("3. Выйти из игры")

        while True:
            choice = input("\nВаш выбор (1-3): ")

            if choice == "1":
                self.start_new_game()
                break
            elif choice == "2":
                self.auth_menu()
                break
            elif choice == "3":
                print("\nДо новых встреч!")
                sys.exit(0)
            else:
                print("Неверный выбор!")

    def play(self):
        if not self.user:
            self.auth_menu()

        self.print_header()
        print(f"\nДОБРО ПОЖАЛОВАТЬ В РОДНОЙ ГОРОД, {self.user.username}!")
        print("\nВы вернулись из Москвы на зимние каникулы.")
        print("Поезд только что прибыл на вокзал.")

        print("\nКуда пойти сначала?")
        print("1. К родителям (домой)")
        print("2. К друзьям (на дачу)")
        print("3. Меню сохранения")

        while True:
            choice = input("\nВаш выбор (1-3): ")

            if choice == "1":
                self.parents_path()
                break
            elif choice == "2":
                self.friends_path()
                break
            elif choice == "3":
                self.save_menu()
                self.print_header()
                print(f"\nДОБРО ПОЖАЛОВАТЬ В РОДНОЙ ГОРОД, {self.user.username}!")
                print("\nВы вернулись из Москвы на зимние каникулы.")
                print("Поезд только что прибыл на вокзал.")
                print("\nКуда пойти сначала?")
                print("1. К родителям (домой)")
                print("2. К друзьям (на дачу)")
                print("3. Меню сохранения")
            else:
                print("Неверный выбор!")


if __name__ == "__main__":
    game = StudentGame()
    game.play()