from abc import ABC, abstractmethod

from src.player import Player


class PlayerInteraction(ABC):
    @classmethod
    @abstractmethod
    def choose_action(cls, player: Player):
        """
        Принимает решение взять карту или использовать фишку
        """
        pass

    @classmethod
    def inform_card_taken(cls, player: Player):
        """
        Сообщает, что игрок взял карту
        """
        pass

    @classmethod
    def inform_card_paid(cls, player: Player):
        """
        Сообщает, что игрок использовал фишку
        """
        pass