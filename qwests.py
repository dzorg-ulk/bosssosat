import random
from game import User

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
