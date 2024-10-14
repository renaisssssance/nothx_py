from src.hand import Hand
from src.card import Card


cards = [Card(13), Card(24), Card(35)]


def test_init():
    a = Hand(cards)
    assert a.cards == cards


def test_repr():
    a = Hand([Card(17)])
    assert a.__repr__() == '[17]'
    assert cards.__repr__() == '[13, 24, 35]'


def test_eq():
    a1 = Hand(cards)
    a2 = Hand(cards)
    a3 = Hand([Card(13), Card(24), Card(35)])
    a4 = Hand([Card(7), Card(9)])
    assert a1 == a2
    assert a1 == a3
    assert a2 != a4
    assert a4 != a3


def test_save():
    a1 = Hand(cards)
    a2 = Hand([Card(5)])
    assert a1.save() == [13, 24, 35]
    assert a2.save() == [5]


def test_load():
    assert Hand.load([13, 24, 35]) == Hand(cards)
    assert Hand.load([9, 17]) == Hand([Card(9), Card(17)])


def test_add_card():
    a = Hand(cards)
    assert repr(a.add_card(Card(25))) == '[13, 24, 35, 25]'
    assert repr(a.add_card(Card(7))) == '[13, 24, 35, 25, 7]'


def test_score():
    h1 = Hand.load([13, 24, 35])
    h2 = Hand.load([3, 4, 5, 13, 25, 17])
    h3 = Hand.load([12, 13, 14, 26, 9, 21, 22, 23])
    assert h1.score() == 72
    assert h2.score() == 58
    assert h3.score() == 68