import enum
import inspect
import json

from src.deck import Deck
from src.game_state import GameState
import src.player_interactions as all_player_types
from src.hand import Hand
from src.player import Player
from src.player_interaction import PlayerInteraction


class GamePhase(enum.StrEnum):
    START_BIDDING = "Draw new card"
    BIDDING = "Choose action: pay or take"
    CONTINUE_BIDDING = "Switch current player due to pay"
    DECLARE_WINNER = "Declare a winner"
    GAME_END = "Game ended"


class GameServer:
    def __init__(self, player_types, game_state):
        self.game_state: GameState = game_state
        self.player_types: dict = player_types

    @classmethod
    def load_game(cls):
        filename = "no_thx.json"
        with open(filename, "r") as f:
            data = json.load(f)
            game_state = GameState.load(data)
            print(game_state.save())
            player_types = {}
            for player, player_data in zip(game_state.players, data["players"]):
                kind = player_data["kind"]
                kind = getattr(all_player_types, kind)
                player_types[player] = kind
            return GameServer(player_types, game_state)

    def save(self):
        filename = "no_thx.json"
        data = self.save_to_dict()
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def save_to_dict(self):
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            player_interaction = self.player_types[player]
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
                player_count = int(input("How many players?"))
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
            name = input("How to call a player?")
            if name.isalpha():
                break
            print("Name must be a single word, alphabetic characters only")

        while True:
            try:
                kind = input(f"What kind of players is it ({player_types_as_str})?")
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
        print(game_state.save())
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
        print(f"{self.game_state.current_player()} is the winner!")
        return GamePhase.GAME_END

    def continue_bidding_phase(self):
        self.game_state.next_player()
        print(f"{self.game_state.current_player()}'s paid")
        return GamePhase.BIDDING

    def start_bidding_phase(self):
        if not self.game_state.deck:
            return GamePhase.DECLARE_WINNER
        self.game_state.curr_card = self.game_state.deck.draw_card()
        self.game_state.curr_chips = 0
        print(f"Top: {self.game_state.curr_card}, chips: {self.game_state.curr_chips}")
        return GamePhase.BIDDING

    def bidding_phase(self):
        current_player = self.game_state.current_player()
        flag = False
        while not flag:
            if PlayerInteraction.choose_action() == "take card":
                self.game_state.take_card()
                flag = True
                PlayerInteraction.inform_card_taken()
            elif PlayerInteraction.choose_action() == "pay card":
                self.game_state.pay_card()
                PlayerInteraction.inform_card_paid()
                return GamePhase.CONTINUE_BIDDING
        return GamePhase.START_BIDDING

    def inform_all(self, method: str, *args, **kwargs):
        for p in self.player_types.values():
            getattr(p, method)(*args, **kwargs)


def __main__():
    load_from_file = False
    if load_from_file:
        server = GameServer.load_game()
        server.save()
    else:
        server = GameServer.new_game(GameServer.get_players())
    server.run()


if __name__ == "__main__":
    __main__()