import logging

class Trick:
    def __init__(self, trick_forehand):
        self.trick_forehand = trick_forehand
        self.cards = []
        self.card_values = 0
        self.trick_winner = None
        self.logger = logging.getLogger(__name__)

    @property
    def leading_card(self):
        return self.cards[0].card if self.cards else None

    @property
    def is_finished(self):
        return len(self.cards) == 3

    def add_move(self, move):
        if len(self.cards) >= 3:
            raise ValueError("Trick is already completed.")

        self.cards.append(move)
        self.card_values += move.card.value

        if self.is_finished:
            self.trick_winner = self.trick_forehand
            if self.cards[1].beats(self.cards[0]):
                self.trick_winner = self.cards[1].player
                if self.cards[2].beats(self.cards[1]):
                    self.trick_winner = self.cards[2].player
            elif self.cards[2].beats(self.cards[0]):
                self.trick_winner = self.cards[2].player

            self.logger.info(f"Trick finished: cards {self.cards} trick winner {self.trick_winner} value {self.card_values}")

    def copy(self):
        copy = Trick(self.trick_forehand)
        copy.cards.extend(self.cards)
        copy.trick_winner = self.trick_winner
        copy.card_values = self.card_values
        return copy
