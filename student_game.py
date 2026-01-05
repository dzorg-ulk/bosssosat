import os
import time
from typing import Optional
import sys

from auth import AuthSystem
from qwests import *
from battle import *

from artifacts import *

class StudentGame:
    def __init__(self):
        self.auth = AuthSystem()
        self.user: Optional[User] = None

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print("*" * 60)
        print("           СТУДЕНТ: ВОЗВРАЩЕНИЕ В РОДНОЙ ГОРОД")
        print("*" * 60)

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
        print("\n" + "*" * 60)
        print("                 ИГРА ЗАВЕРШЕНА!")
        print("*" * 60)

        print(f"\nПОЗДРАВЛЯЕМ, {self.user.username}!")
        print("Вы завершили все квесты в родном городе!")

        print("\n" + "*" * 60)
        print("ВАШИ РЕЗУЛЬТАТЫ:")
        print("*" * 60)

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

        print("\n" + "*" * 60)
        print("ОБЩИЙ ВЫВОД:")
        print("*" * 60)

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

        print("\n" + "*" * 60)

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
                artifacts = load_artifacts()
                self.add_artifact(artifacts["Чаепитие"])
                clear_artifacts(artifacts, "Чаепитие")


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
                    artifacts = load_artifacts()
                    self.add_artifact(artifacts["Анекдотер"])
                    clear_artifacts(artifacts, "Анекдотер")

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
        artifacts = load_artifacts()
        self.add_artifact(artifacts["Уличная жизнь"])
        clear_artifacts(artifacts, "Уличная жизнь")

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

                for i in range(3):
                    random_text = ''.join(random.choices('абвгдеёжзийклмнопрстуфхцчшщъыьэюя !?;,.', k=40))
                    print("\nДруг:", "'", f"{random_text}", "'")
                    time.sleep(1)
                    if i < 2:
                        input("Вы: 'Чего-чего?...'")

                print("\nЭффект зелья прошел!")
                break
            elif choice == "2":
                print("\nВы: 'Нет, спасибо, я и так в норме.'")
                print("\nДруг(кому-то за спиной): 'Чувак, аккуратнее!'")
                time.sleep(1)
                print("\nВы слышите, как что-то разбивается вдребезги")
                time.sleep(1)
                break
            else:
                print("Неверный выбор!")

        print("\nДруг: 'Только не ящик пива... Придется посылать гонца за добавкой'")
        time.sleep(3)
        print("Друг: 'Сыграем в камень-ножницы-бумага?'")

        input("\nНажмите Enter для игры...")

        rps_result = RockPaperScissors.play()

        if rps_result == "win":
            print("\nВЫ ВЫИГРАЛИ!")
            print("Друзья: 'Ну ты везунчик!'")

            artifacts = load_artifacts()
            self.add_artifact(artifacts["Гонец"])
            clear_artifacts(artifacts, "Гонец")

            self.user.drunk_level += 20
            self.user.quests_completed["rps_game"] = True

            if self.check_all_quests_completed():
                self.game_completed()
                return

            self.after_party_choice()

        else:
            print("\nВЫ ПРОИГРАЛИ!")
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
                artifacts = load_artifacts()
                self.add_artifact(artifacts["Экономист"])
                clear_artifacts(artifacts, "Экономист")
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
