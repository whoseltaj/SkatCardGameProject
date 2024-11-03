from card import Card
from typing import List, Optional

class Hand:
    def __init__(self, cards: List[Card], round_context):
        self.cards: List[Card] = cards
        self.round_context = round_context
        self.jacks = self.get_jacks()
        self.set_cards_round()
        self.tricks: List[List[Card]] = []

    def get_tricks(self) -> List[List[Card]]:
        return self.tricks

    def get_points(self) -> int:
        return sum(trick.get_points() for trick in self.tricks)

    def get_number_of_tricks(self) -> int:
        return len(self.tricks)

    def sort_hand(self) -> None:
        if self.round_context.is_grand():
            self.sort_hand_for_grand()
        elif self.round_context.is_suit():
            self.sort_hand_for_suit()
        else:
            self.sort_hand_for_null()

    def sort_hand_for_null(self) -> None:
        self.cards.sort(key=lambda card: (4 - card.suit.value, card.face.value), reverse=True)

    def sort_hand_for_grand(self) -> None:
        self.sort_hand_for_null()
        ordered_cards = self.get_jacks()
        ordered_cards.extend(self.get_cards_from_non_trump_suits())
        self.cards = ordered_cards

    def sort_hand_for_suit(self) -> None:
        self.sort_hand_for_null()
        ordered_cards = self.get_jacks()
        ordered_cards.extend(self.get_cards_from_trump_suit())
        ordered_cards.extend(self.get_cards_from_non_trump_suits())
        self.cards = ordered_cards

    def get_cards_from_trump_suit(self) -> List[Card]:
        return self.get_cards_depending_on_trump_status(True)

    def get_cards_from_non_trump_suits(self) -> List[Card]:
        return self.get_cards_depending_on_trump_status(False)

    def get_cards_depending_on_trump_status(self, trump: bool) -> List[Card]:
        return [card for card in self.cards if card.is_trump() == trump and not card.is_jack()]

    def set_cards_round(self) -> None:
        for card in self.cards:
            card.set_round(self.round_context)

    def has_card(self, card: Card) -> bool:
        return card in self.cards

    def has_suit(self, suit: Card.Suit) -> bool:
        return any(card.suit == suit for card in self.cards)

    def has_face(self, face: Card.Face) -> bool:
        return any(card.face == face for card in self.cards)

    def get_jack_multiplier(self) -> int:
        if self.has_first_jack():
            return self.get_lowest_successive_jack().suit.value + 1
        return self.get_highest_jack().suit.value if self.jacks else 4

    def get_jacks(self) -> List[Card]:
        jacks = [card for card in self.cards if card.face == Card.Face.JACK]
        jacks.sort(key=lambda card: card.suit.value)
        return jacks

    def get_lowest_successive_jack(self) -> Card:
        if len(self.jacks) == 1:
            return self.jacks[0]
        for i in range(len(self.jacks) - 1):
            if self.jacks[i].suit.value + 1 != self.jacks[i + 1].suit.value:
                return self.jacks[i]
        return self.jacks[-1]

    def get_highest_jack(self) -> Optional[Card]:
        return self.jacks[0] if self.jacks else None

    def get_lowest_jack(self) -> Optional[Card]:
        return self.jacks[-1] if self.jacks else None

    def lay_card(self, card: Card) -> Optional[Card]:
        if card in self.cards:
            self.cards.remove(card)
            return card
        return None

    def has_first_jack(self) -> bool:
        return any(card == Card(Card.Suit.CLUB, Card.Face.JACK) for card in self.jacks)

    def __repr__(self) -> str:
        return f"Hand({self.cards})"
