import random
from src.card import Card


class Deck:
    def __init__(self, cards: None | list[Card]):
        if cards is None:
            cards = Card.all_cards()
            random.shuffle(cards)
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


    def draw_card(self):
        return self.cards.pop()


    def shuffle(self):
        random.shuffle(self.cards)