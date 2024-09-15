class Card:
    VALUES = list(range(3, 36))

    def __init__(self, value):
        if value not in Card.VALUES:
            raise ValueError
        self.value = value

    def __repr__(self):
        return f'<{self.value}>'