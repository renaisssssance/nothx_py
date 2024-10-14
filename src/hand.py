from src.card import Card


class Hand:
    def __init__(self, cards: list[Card] = None):
        if cards is None:
            cards = []
        self.cards: list[Card] = cards

    def __repr__(self):
        return f"{self.cards}"

    def __eq__(self, other):
        if isinstance(other, list):
            other = Hand.load(other)
        return self.cards == other.cards

    def save(self):
        return [c.save() for c in self.cards]

    @classmethod
    def load(cls, res: list[int]):
        return cls(cards=[Card.load(item) for item in res])

    def add_card(self, card: Card):
        self.cards.append(card)
        return self

    def score(self):
        a = [c.value for c in self.cards]
        a.sort()
        s = 0
        last, current = 0, 0
        while a:
            last, current = current, a.pop()
            if last != 0 and last - current == 1:
                continue
            s += last
        s += current
        return s