import json
import typing

from src.hand import Hand


class Player:
    def __init__(self, name: str, hand: Hand, chips: int = 11):
        self.name = name
        self.hand = hand
        self.chips = chips

    def __repr__(self):
        return f"{self.name}({self.chips}): {self.hand}"

    def __eq__(self, other: typing.Self | str | dict):
        if isinstance(other, str):
            other = self.load(json.loads(other))
        if isinstance(other, dict):
            other = self.load(other)
        return (
            self.name == other.name
            and self.chips == other.chips
            and self.hand == other.hand
        )

    def __hash__(self):
        return hash(self.name)

    def save(self):
        return {"name": self.name, "hand": self.hand, "chips": self.chips}

    @classmethod
    def load(cls, data: dict):
        return cls(
            name=data["name"], hand=Hand.load(data["hand"]), chips=int(data["chips"])
        )

    def score(self):
        return self.hand.score() - self.chips