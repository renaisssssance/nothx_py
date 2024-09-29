import random
from src.card import Card
from src.deck import Deck


cards = [Card(13), Card(24), Card(35)]


def test_init():
    a = Deck(cards)
    assert a.cards == cards


def test_init_shuffle():
    a1 = Deck(None)
    a2 = Deck(None)
    assert a1.cards != a2.cards


def test_repr():
    a = Deck([Card(17)])
    assert a.__repr__() == '[17]'
    assert cards.__repr__() == '[13, 24, 35]'


def test_eq():
    a1 = Deck(cards)
    a2 = Deck(cards)
    a3 = Deck([Card(13), Card(24), Card(35)])
    a4 = Deck([Card(7), Card(9)])
    assert a1 == a2
    assert a1 == a3
    assert a2 != a4
    assert a4 != a3


def test_save():
    a1 = Deck(cards)
    a2 = Deck([Card(5)])
    assert a1.save() == [13, 24, 35]
    assert a2.save() == [5]


def test_load():
    assert Deck.load([13, 24, 35]) == Deck(cards)
    assert Deck.load([9, 17]) == Deck([Card(9), Card(17)])


def test_draw_card():
    a1 = Deck(cards)
    assert a1.draw_card() == Card(35)
    assert a1 == Deck([Card(13), Card(24)])


def test_shuffle():
    random.seed(3)
    c = Card.all_cards([20, 21, 22, 23, 24, 25])
    deck = Deck(c)
    deck.shuffle()
    assert deck.save() == [20, 22, 23, 25, 24, 21]
    deck.shuffle()
    assert deck.save() == [22, 25, 23, 20, 24, 21]
    deck.shuffle()
    assert deck.save() == [24, 21, 22, 25, 23, 20]