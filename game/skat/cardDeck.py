import random
from game.skat.cards import Card
from enum import Enum

class Card:
    # Represents a card in a Skat deck with suits and faces.
    
    class Face(Enum):
        SEVEN = 0
        EIGHT = 1
        NINE = 2
        TEN = 3
        JACK = 4
        QUEEN = 5
        KING = 6
        ACE = 7

        @staticmethod
        def to_display(face):
            # Return a display-friendly version of the face.
            face_display = {
                Card.Face.SEVEN: '7',
                Card.Face.EIGHT: '8',
                Card.Face.NINE: '9',
                Card.Face.TEN: '10',
                Card.Face.JACK: 'J',
                Card.Face.QUEEN: 'Q',
                Card.Face.KING: 'K',
                Card.Face.ACE: 'A'
            }
            return face_display.get(face, '')

        @classmethod
        def list(cls):
            # Return a list of all faces.
            return list(cls)

    class Suit(Enum):
        CLUB = 0
        SPADE = 1
        HEARTS = 2
        DIAMOND = 3

        @staticmethod
        def to_display(suit):
            # Return a display-friendly version of the suit.
            suit_display = {
                Card.Suit.CLUB: '♣',
                Card.Suit.SPADE: '♠',
                Card.Suit.HEARTS: '♥',
                Card.Suit.DIAMOND: '♦'
            }
            return suit_display.get(suit, '')

        @classmethod
        def list(cls):
            # Return a list of all suits.
            return list(cls)

    def __init__(self, suit, face):
        # Initialize a card with a suit and face.
        self.suit = suit
        self.face = face
        self.round = None  # The round or context in which the card is played.

    def has_suit(self, suit):
        # Check if the card has the given suit.
        return self.suit == suit

    def has_face(self, face):
        # Check if the card has the given face.
        return self.face == face

    def get_value(self):
        # Return the point value of the card for scoring.
        face_values = {
            Card.Face.JACK: 2,
            Card.Face.ACE: 11,
            Card.Face.TEN: 10,
            Card.Face.KING: 4,
            Card.Face.QUEEN: 3
        }
        return face_values.get(self.face, 0)

    @staticmethod
    def jack_list():
        # Return a list of all Jacks in the deck.
        return [Card(suit, Card.Face.JACK) for suit in Card.Suit.list()]

    def set_round(self, round):
        # Set the round context for the card.
        self.round = round

    def get_round(self):
        # Return the round context of the card.
        return self.round

    def is_trump(self):
        # Determine if the card is a trump card.
        if self.round.is_NULL():
            return False
        elif self.round.is_grand():
            return self.has_face(Card.Face.JACK)
        elif self.round.is_suit():
            return self.suit == self.round.get_type() or self.has_face(Card.Face.JACK)

    def is_jack(self):
        # Check if the card is a Jack.
        return self.has_face(Card.Face.JACK)

    def is_not_jack(self):
        # Check if the card is not a Jack.
        return not self.is_jack()

    def is_greater_NULL_game(self, other):
        # Determine if the card is greater than another card in a NULL game.
        if self.has_suit(other.suit):
            return self.face.value > other.face.value
        return False

    def is_less_NULL_game(self, other):
        # Determine if the card is less than another card in a NULL game.
        return not self.is_greater_NULL_game(other)

    def is_greater_non_NULL_game(self, other):
        # Determine if the card is greater than another card in a non-NULL game.
        
        # The current card is trump or a Jack while the other card isn't.
        if self.is_trump() and not other.is_trump() or self.is_jack() and other.is_not_jack():
            return True

        # Both cards are Jacks; compare their suits.
        elif self.is_jack() and other.is_jack():
            return self.suit.value < other.suit.value

        # Both cards have the same suit, and the other is not a Jack.
        elif self.has_suit(other.suit) and other.is_not_jack():
            return self.face.value > other.face.value

        # In all other cases, the current card is not greater.
        return False

    def is_less_non_NULL_game(self, other):
        # Determine if the card is less than another card in a non-NULL game.
        return not self.is_greater_non_NULL_game(other)

    def __repr__(self):
        # Return a string representation of the card.
        return f"{Card.Face.to_display(self.face)}{Card.Suit.to_display(self.suit)}"

    def __eq__(self, other):
        # Check if two cards are equal.
        return isinstance(other, Card) and self.suit == other.suit and self.face == other.face

    def __ne__(self, other):
        # Check if two cards are not equal.
        return not self.__eq__(other)

    def __hash__(self):
        # Return the hash of the card.
        return hash((self.suit, self.face))

    def __gt__(self, other):
        # Determine if this card is greater than another.
        if self.round.is_NULL():
            return self.is_greater_NULL_game(other)
        else:
            return self.is_greater_non_NULL_game(other)

    def __ge__(self, other):
        # Determine if this card is greater than or equal to another.
        return self == other or self > other

    def __lt__(self, other):
        # Determine if this card is less than another.
        if self.round.is_NULL():
            return self.is_less_NULL_game(other)
        else:
            return self.is_less_non_NULL_game(other)

    def __le__(self, other):
        # Determine if this card is less than or equal to another.
        return self == other or self < other
