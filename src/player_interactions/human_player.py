from src.player import Player
from src.player_interaction import PlayerInteraction


class Human(PlayerInteraction):
    @classmethod
    def choose_action(cls, player: Player):
        while True:
            print("Choose action: type 't' or 'p' (take card or pay)\n")
            action = input()
            if action == "t":
                return 'take card'
            elif action == "p":
                if player.chips <= 0:
                    print("You have no chips, action replaced by take card")
                    return 'take card'
                return 'pay'
            else:
                continue

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