from enum import Enum

class Player:
    class Type(Enum):
        DECLARER = 0
        DEFENDER = 1

    def __init__(self, name):
        self.name = name
        self.type = None
        self.hand = None
        self.tricks = []

    def add_trick(self, trick):
        self.tricks.append(trick)
        return True

    def get_tricks_from_round(self, round):
        return [trick for trick in self.tricks if trick.get_round() == round] if self.tricks else []

    def set_hand(self, hand):
        self.hand = hand

    def get_hand(self):
        return self.hand

    def sum_trick_values(self):
        total_value = 0
        for trick in self.tricks:
            for card in trick:
                total_value += card.get_value()
        return total_value

    def has_card(self, card):
        return card in self.hand

    def has_suit(self, suit):
        return any(card.suit == suit for card in self.hand)

    def has_face(self, face):
        return any(card.face == face for card in self.hand)

    def __repr__(self):
        return f"Player(name={self.name}, hand={self.hand})"

    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)
