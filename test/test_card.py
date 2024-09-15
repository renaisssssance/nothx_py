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

def test_repr():
    a = Card(34)
    assert a.__repr__() == '<34>'