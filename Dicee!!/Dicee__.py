import random

class Die:
    def __init__(self, sides=6):
        self.sides = sides  # кількість граней на кістці
        self.value = 1  # початкове значення кістки

    def roll(self):
        """Генеруємо випадкове значення для кістки"""
        self.value = random.randint(1, self.sides)

    def get_value(self):
        """Повертаємо значення кістки"""
        return self.value


class DiceGame:
    def __init__(self, num_players=2, num_dice=2):
        self.num_players = num_players  # кількість гравців
        self.num_dice = num_dice  # кількість кісток для кожного гравця
        self.players_scores = [0] * self.num_players  # підсумкові бали кожного гравця
        self.dice = [Die() for _ in range(num_dice)]  # список для кісток

    def roll_all_dice(self):
        """Кидаємо всі кістки для кожного гравця"""
        for die in self.dice:
            die.roll()

    def calculate_score(self):
        """Обчислюємо суму результатів всіх кісток"""
        return sum(die.get_value() for die in self.dice)

    def play_round(self):
        """Один раунд гри для всіх гравців"""
        for i in range(self.num_players):
            input(f"Гравець {i + 1}, натисніть Enter, щоб кинути кістки...")
            print(f"Гравець {i + 1} кидає кістки:")
            self.roll_all_dice()
            score = self.calculate_score()
            self.players_scores[i] += score
            print(f"Результат гравця {i + 1}: {score}")
        self.display_scores()

    def display_scores(self):
        """Показуємо поточні бали всіх гравців"""
        print("\nПоточні бали:")
        for i in range(self.num_players):
            print(f"Гравець {i + 1}: {self.players_scores[i]}")


if __name__ == "__main__":
    game = DiceGame(num_players=2, num_dice=2)  # Створюємо гру для 2 гравців, 2 кістки кожному
    rounds = 3  # Кількість раундів
    for round_number in range(1, rounds + 1):
        print(f"\nРаунд {round_number}")
        game.play_round()

