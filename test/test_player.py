from src.hand import Hand
from src.player import Player


def test_init():
    h = Hand.load([13, 14, 25])
    p = Player(name="Alex", hand=h, chips=17)
    assert p.name == "Alex"
    assert p.hand == h
    assert p.chips == 17


def test_repr():
    h = Hand.load([13, 14, 25])
    p = Player(name="Alex", hand=h, chips=17)
    assert repr(p) == "Alex(17): [13, 14, 25]"


def test_eq():
    h = Hand.load([13, 14, 25])
    p1 = Player(name="Alex", hand=h, chips=17)
    p2 = Player(name="Alex", hand=h, chips=17)
    assert p1 == p2


def test_save():
    h = Hand.load([13, 14, 25])
    p = Player(name="Alex", hand=h, chips=17)
    assert p.save() == {"name": "Alex", "chips": 17, "hand": [13, 14, 25]}


def test_load():
    d = {"name": "Alex", "chips": 17, "hand": [13, 14, 25]}
    h = Hand.load([13, 14, 25])
    p_expected = Player(name="Alex", hand=h, chips=17)
    p = Player.load(d)
    assert  p == p_expected