import pytest
from src.card import Card


def test_init():
    a = Card(25)
    assert a.value == 25
    with pytest.raises(ValueError):
        Card(1)
    with pytest.raises(ValueError):
        Card(100)
    with pytest.raises(ValueError):
        Card(1.15)
    with pytest.raises(ValueError):
        Card('t')
    with pytest.raises(ValueError):
        Card('25')
    with pytest.raises(ValueError):
        Card(-15)


def test_repr():
    a = Card(34)
    assert a.__repr__() == '34'


def test_eq():
    c1 = Card(31)
    c2 = Card(31)
    c3 = Card(11)
    c4 = Card(7)
    c5 = Card(11)
    assert c1 == c2
    assert c1 != c3
    assert c3 == c5
    assert c4 != c1


def test_save():
    c = Card(31)
    assert c.save() == 31


def test_load():
    c1 = Card(31)
    c2 = 31
    assert Card.load(c2) == c1
    c3 = 25
    c4 = Card.load(c3)
    assert c4 == Card(25)


def test_all_cards():
    cards = Card.all_cards([3, 35, 14, 27, 19])
    expected_cards = [
        Card.load(3),
        Card.load(35),
        Card.load(14),
        Card.load(27),
        Card.load(19)
    ]
    assert cards == expected_cards
    cards = Card.all_cards()
    assert len(cards) == 33


def test_score():
    c1 = Card(7)
    c2 = Card(25)
    assert c1.score() == 7
    assert c2.score() == 25