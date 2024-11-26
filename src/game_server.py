import enum
import inspect
import json
from operator import itemgetter
from pathlib import Path

from src.deck import Deck
from src.game_state import GameState
import src.player_interactions as all_player_types
from src.hand import Hand
from src.player import Player
from src.player_interaction import PlayerInteraction


class GamePhase(enum.StrEnum):
    START_BIDDING = "Draw new card"
    BIDDING = "Choose action: take card or pay"
    CONTINUE_BIDDING = "Switch current player due to pay"
    DECLARE_WINNER = "Declare a winner"
    GAME_END = "Game ended"


class GameServer:
    def __init__(self, player_types, game_state):
        self.game_state: GameState = game_state
        self.player_types: dict = player_types

    @classmethod
    def load_game(cls, filename: str | Path):
        with open(filename, "r") as f:
            data = json.load(f)
            game_state = GameState.load(data)
            # print(game_state.save())
            player_types = {}
            for player, player_data in zip(game_state.players, data["players"]):
                kind = player_data["kind"]
                kind = getattr(all_player_types, kind)
                player_types[player] = kind
            return GameServer(player_types, game_state)

    def save(self, filename: str | Path):
        data = self.save_to_dict()
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def save_to_dict(self):
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            data["players"][player_index]["kind"] = self.player_types[player].__name__
        return data

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()
        player_types = {}
        for p in range(player_count):
            name, kind = cls.request_player()
            player = Player(name, Hand())
            player_types[player] = kind
        return player_types

    @staticmethod
    def request_player_count():
        while True:
            try:
                player_count = int(input("How many players?\n"))
                if 3 <= player_count <= 5:
                    return player_count
            except ValueError:
                pass
            print("Please input a number between 3 and 5")

    @staticmethod
    def request_player():
        player_types = []
        for name, cls in inspect.getmembers(all_player_types):
            if inspect.isclass(cls) and issubclass(cls, PlayerInteraction):
                player_types.append(cls.__name__)
        player_types_as_str = ', '.join(player_types)

        while True:
            name = input("How to call a player?\n")
            if name.isalpha():
                break
            print("Name must be a single word, alphabetic characters only")

        while True:
            try:
                kind = input(f"What kind of players is it ({player_types_as_str})?\n")
                kind = getattr(all_player_types, kind)
                break
            except AttributeError:
                print(f"Allowed player types are: {player_types_as_str}")
        return name, kind

    @classmethod
    def new_game(cls, player_types):
        deck = Deck().full_deck()
        top = deck.draw_card()
        game_state = GameState(list(player_types.keys()), deck, top)
        res = cls(player_types, game_state)
        return res

    def run(self):
        current_phase = GamePhase.BIDDING
        while current_phase != GamePhase.GAME_END:
            phases = {
                GamePhase.START_BIDDING: self.start_bidding_phase,
                GamePhase.BIDDING: self.bidding_phase,
                GamePhase.CONTINUE_BIDDING: self.continue_bidding_phase,
                GamePhase.DECLARE_WINNER: self.declare_winner_phase
            }
            current_phase = phases[current_phase]()

    def declare_winner_phase(self):
        score = self.game_state.score_players()
        sorted_score = sorted(score.items(), key=itemgetter(1))
        print("Leaderboard:")
        for index, (p, s) in enumerate(sorted_score, start=1):
            print(f"{index}. {p}, score={s}")
        print(f"{sorted_score[0][0]} is the winner!")
        return GamePhase.GAME_END

    def continue_bidding_phase(self):
        self.game_state.next_player()
        return GamePhase.BIDDING

    def start_bidding_phase(self):
        if self.game_state.deck == Deck([]):
            return GamePhase.DECLARE_WINNER
        self.game_state.curr_card = self.game_state.deck.draw_card()
        self.game_state.curr_chips = 0
        return GamePhase.BIDDING

    def bidding_phase(self):
        current_player = self.game_state.current_player()
        print(f"Top: {self.game_state.curr_card}, chips: {self.game_state.curr_chips}")
        print(f"Move: {self.game_state.current_player()}")
        player = self.player_types[current_player]
        action = player.choose_action(current_player)
        if action == 'take card':
            self.game_state.take_card()
            print(f"{self.game_state.current_player().name}'s taken")
            # player.inform_card_taken()
            return GamePhase.START_BIDDING
        elif action == 'pay':
            self.game_state.pay_card()
            print(f"{self.game_state.current_player().name}'s paid")
            # player.inform_card_paid()
            return GamePhase.CONTINUE_BIDDING

    def inform_all(self, method: str, *args, **kwargs):
        for p in self.player_types.values():
            getattr(p, method)(*args, **kwargs)


def __main__():
    load_from_file = False
    if load_from_file:
        server = GameServer.load_game("no_thx.json")
    else:
        server = GameServer.new_game(GameServer.get_players())
    server.save("no_thx_savefile.json")
    server.run()


if __name__ == "__main__":
    __main__()