from src.card import Card


class Hand:
    def __init__(self, cards: list[Card] = None):
        if cards is None:
            cards = []
        self.cards: list[Card] = cards


    def __repr__(self):
        return f'{self.cards}'


    def __eq__(self, other):
        return self.cards == other.cards


    def save(self):
        return [c.save() for c in self.cards]


    @classmethod
    def load(cls, res: list[int]):
        return cls(cards=[Card.load(item) for item in res])


    def add_card(self, card: Card):
        self.cards.append(card)
        return self