from src.card import Card
from src.deck import Deck
from src.game_state import GameState
from src.player import Player

data = {
    "top": {"card": 9, "chips": 0},
    "deck": [15, 31, 28, 9, 20],
    "current_player_index": 0,
    "players": [
        {
            "name": "Bot_Alex",
            "chips": 27,
            "hand": [30, 11, 4, 27, 7],
        },
        {
            "name": "Bob",
            "chips": 14,
            "hand": [3, 17, 19, 33],
        },
        {
            "name": "Steve",
            "chips": 18,
            "hand": [5, 6, 23, 21],
        },
    ],
}

Bot_Alex = Player.load(data["players"][0])
Bob = Player.load(data["players"][1])
Steve = Player.load(data["players"][2])
full_deck = Deck(None)


def test_init():
    players = [Bot_Alex, Bob, Steve]
    game = GameState(
        players=players, deck=full_deck, curr_card=Card(7), curr_chips=11, curr_player=1
    )
    assert game.players == players
    assert game.deck == full_deck
    assert game.curr_card == Card(7)
    assert game.curr_chips == 11
    assert game._curr_player == 1


def test_current_player():
    players = [Bot_Alex, Bob, Steve]
    for i, player in enumerate(players):
        game = GameState(
            players=players,
            deck=full_deck,
            curr_card=Card(7),
            curr_chips=11,
            curr_player=i,
        )
        assert game.current_player() == player


def test_save():
    players = [Bot_Alex, Bob, Steve]
    game = GameState(
        players=players,
        deck=Deck.load(data["deck"]),
        curr_card=Card.load(data["top"]["card"]),
        curr_chips=data["top"]["chips"],
        curr_player=0,
    )
    assert game.save() == data


def test_load():
    game = GameState.load(data)
    assert game.save() == data


def test_next_player():
    game = GameState.load(data)
    assert game.current_player() == Bot_Alex
    game.next_player()
    assert game.current_player() == Bob
    game.next_player()
    assert game.current_player() == Steve
    game.next_player()
    assert game.current_player() == Bot_Alex


def test_draw_card():
    game = GameState.load(data)
    assert game.deck == [15, 31, 28, 9, 20]
    assert game.current_player().hand == [30, 11, 4, 27, 7]
    game.draw_card()
    assert game.deck == [15, 31, 28, 9]
    assert game.current_player().hand == [30, 11, 4, 27, 7, 20]