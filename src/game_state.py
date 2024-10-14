from src.card import Card
from src.deck import Deck
from src.player import Player


class GameState:
    def __init__(
        self,
        players: list[Player],
        deck: Deck,
        curr_card: Card,
        curr_chips: int = 0,
        curr_player: int = 0,
    ):
        self.players = players
        self.deck = deck
        self.curr_card = curr_card
        self.curr_chips = curr_chips
        self._curr_player = curr_player

    def current_player(self):
        return self.players[self._curr_player]

    def __eq__(self, other):
        other: GameState
        return (
            self.players == other.players
            and self.deck == other.deck
            and self.curr_card == other.curr_card
            and self.curr_chips == other.curr_chips
            and self._curr_player == other._curr_player
        )

    def save(self):
        return {
            "top": {"card": self.curr_card, "chips": self.curr_chips},
            "deck": self.deck,
            "current_player_index": self._curr_player,
            "players": [p.save() for p in self.players],
        }

    @classmethod
    def load(cls, data: dict):
        players = [Player.load(d) for d in data["players"]]
        return cls(
            players=players,
            deck=Deck.load(data["deck"]),
            curr_card=Card.load(data["top"]["card"]),
            curr_chips=data["top"]["chips"],
            curr_player=data["current_player_index"],
        )

    def next_player(self):
        self._curr_player += 1
        self._curr_player %= len(self.players)

    def draw_card(self):
        card = self.deck.draw_card()
        self.current_player().hand.add_card(card)
        return card