import random
from itertools import combinations

Selection = ["Scissors", "Rock", "Paper"]


class Player:
    Player_dict = {}

    def get_choice(self):
        while True:
            try:
                choice = int(input("Shape your destiny: 1 for Scissors, "
                                   "2 for Rock, 3 for Paper: "))
                if 1 <= choice <= 3:
                    return choice - 1
                else:
                    print("Choose a number from 1 to 3 to start.")
            except ValueError:
                print("Uh-oh! It seems like we're on a detour.\n"
                      "Provide a proper map with a valid number, adventurer!")

    choice = property(get_choice)

    def add_player(self, player_type):
        choice = self.choice
        self.Player_dict[f"{len(self.Player_dict) + 1}"] = {
            player_type: [choice]}


class BOT(Player):
    def get_choice(self):
        return 1

    choice = property(get_choice)


class Easy(BOT):
    def __init__(self):
        super().__init__()

    def get_choice(self):
        if not hasattr(self, "random_choice"):
            self.random_choice = random.randint(0, 2)
        else:
            self.random_choice = (self.random_choice + 1) % 3
        return self.random_choice

    choice = property(get_choice)


class Medium(BOT):
    def __init__(self):
        super().__init__()
        self.last_move = None

    def get_choice(self):
        if self.last_move is None:
            return random.randint(0, 2)
        else:
            return self.last_move

    def update_last_move(self, l_move, l_moves):
        self.last_move = l_moves[l_move] if l_move in l_moves else l_move

    choice = property(get_choice)


class Hard(BOT):
    def get_choice(self):
        return random.randint(0, 2)

    choice = property(get_choice)


class GameEngine:
    @staticmethod
    def result(index1, index2, choice1, choice2, scores):
        if choice1 == choice2:
            scores[index1] += 1
            scores[index2] += 1
            return f"Draw - Both players get 1 point"
        elif (choice1 + 1) % 3 == choice2:
            scores[index2] += 2
            return f"Player {index2} wins - Player {index2} gets 2 points"
        else:
            scores[index1] += 2
            return f"Player {index1} wins - Player {index1} gets 2 points"


class Game:
    def __init__(self, rounds, players_dict):
        self.rounds = rounds
        self.players_dict = players_dict
        self.players = list(self.get_players_from_dict())
        self.player_choices = {}
        self.last_moves = {}

    def run_game(self):
        player_combinations = list(
            combinations(
                enumerate(
                    self.players[0],
                    start=1),
                2))
        scores = {index: 0 for index in range(1, len(self.players[0]) + 1)}
        self.player_choices = {}

        for round_num in range(1, self.rounds + 1):
            if len(self.players[0]) < 2:
                print("Add at least two players to start the game!"
                      "🚀 Let the games begin!")
                return

            print(f"\n                        Round {round_num}/{self.rounds}")

            for (i1, player1), (i2, player2) in player_combinations:
                print(
                    f" --- Player {i1} --- --- --- vs. --- Player {i2} ---")

                # Ändere die Zeile unten
                choice1 = player1.get_choice()
                choice2 = player2.get_choice()

                self.player_choices.setdefault(i1, []).append(choice1)
                self.player_choices.setdefault(i2, []).append(choice2)

                if isinstance(player1, Medium):
                    player1.update_last_move(choice2, self.last_moves)
                if isinstance(player2, Medium):
                    player2.update_last_move(choice1, self.last_moves)

                print(
                    f"  🎮 Player {i1} choose {Selection[choice1]}   |   "
                    f"Player {i2} choose {Selection[choice2]}\n"
                    f"    🏆 Result: "
                    f"{GameEngine.result(i1, i2, choice1, choice2, scores)}\n")

        print("🏁 Game Over! Final Scores:")
        for rank, (player, score) in enumerate(
            sorted(scores.items(), key=lambda x: x[1], reverse=True), start=1
        ):
            print(f"  Player {player} got {score} points: Rank {rank}")

        self.show_player_choices()

        input("\nPress Enter to continue...")

    def show_player_choices(self):
        if not self.player_choices:
            print("Oops! It seems like the game history is a mystery. "
                  "Play a game to script some epic tales!")
            return

        print("\n--- 📜  Peek into History ---")
        for index, choices in self.player_choices.items():
            player = self.players[0][index - 1]
            choice_strings = [Selection[choice] for choice in choices]
            print(
                f"Player {index} "
                f"(Type: {type(player).__name__}): {choice_strings}")

    def get_players_from_dict(self):
        last_moves = {}
        players = []
        for key, player_info in Player().Player_dict.items():
            player_type, choices = list(player_info.items())[0]
            player_instance = self.create_player_instance(player_type)
            if isinstance(player_instance, Medium):
                last_moves[key] = player_instance
            players.append(player_instance)

        return players, last_moves

    def create_player_instance(self, player_type):
        if player_type == "BOT":
            return BOT()
        elif player_type == "Easy":
            return Easy()
        elif player_type == "Medium":
            return Medium()
        elif player_type == "Hard":
            return Hard()
        else:
            return Player()


class Menu:
    def __init__(self, initial_rounds):
        self.rounds = initial_rounds
        self.game = Game(self.rounds, [])

        self.menu_setup = {
            "➕  Summon a New Player": {
                "🧑 Player": lambda: self.add_player_menu("Player"),
                "✊ BOT (Always Rock)": lambda: self.add_player_menu("BOT"),
                "🔄 Easy (Routine Spin)": lambda: self.add_player_menu("Easy"),
                "🤖 Medium (Mimicking)": lambda: self.add_player_menu("Medium"),
                "🎲 Hard (Random Chaos)": lambda: self.add_player_menu("Hard"),
            },
            "🔢  Explore Rounds": self.set_rounds,
            "📜  Peek into History": self.game.show_player_choices,
            "🎮  Dive into the Action": self.game.run_game,
        }

    def show_rounds(self):
        print(f"\nNumber of Rounds: {self.rounds}")

    def set_rounds(self):
        try:
            new_rounds = int(input("Enter the number of rounds: "))
            if new_rounds > 0:
                self.rounds = new_rounds
                self.game.rounds = new_rounds
                print(f"Number of rounds set to {new_rounds}")
            else:
                print("Please enter a positive number of rounds.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def add_player_menu(self, player_type):
        player_instance = self.game.create_player_instance(player_type)
        self.game.players[0].append(player_instance)
        print(f"Player of type {player_type} added.")

    def display_menu(self):
        while True:
            print("\n--- Game Hub ---")
            for i, option in enumerate(self.menu_setup, start=1):
                print(f"{i}. {option} (Input: {i})")

            user_input = input("Your choice (q to quit): ")

            if user_input.lower() == "q":
                break
            else:
                try:
                    choice = int(user_input)
                    if 1 <= choice <= len(self.menu_setup):
                        selected_o = list(self.menu_setup.keys())[choice - 1]
                        if callable(self.menu_setup[selected_o]):
                            self.menu_setup[selected_o]()
                        elif isinstance(self.menu_setup[selected_o], dict):
                            submenu = Menu(self.rounds)
                            submenu.menu_setup = self.menu_setup[selected_o]
                            submenu.display_menu()
                except ValueError:
                    print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    initial_rounds = 3

    print('''
    Welcome to the Rock-Paper-Scissors Game!
    To start, add at least two players.
    The default setting is {} rounds.
    The history will be available after completing a game.
    '''.format(initial_rounds))

    main_menu = Menu(initial_rounds)
    main_menu.display_menu()
