import logging
from typing import List, Optional, Any

class Trick:
    def __init__(self, trick_forehand: 'Player'):
        self.trick_forehand = trick_forehand
        self.cards: List['Move'] = []
        self.card_values: int = 0
        self.trick_winner: Optional['Player'] = None
        self.logger = logging.getLogger(__name__)

    @property
    def leading_card(self) -> Optional['Card']:
        return self.cards[0].card if self.cards else None

    @property
    def is_finished(self) -> bool:
        return len(self.cards) == 3

    def add_move(self, move: 'Move') -> None:
        if self.is_finished:
            raise ValueError("Cannot add move; trick is already completed.")

        self.cards.append(move)
        self.card_values += move.card.value

        self.logger.debug(f"Move added: {move}. Current trick state: {self.cards}")

        if self.is_finished:
            self.determine_winner()
            self.logger.info(
                f"Trick finished: cards {self.cards}, trick winner {self.trick_winner}, total value {self.card_values}"
            )

    def determine_winner(self) -> None:
        self.trick_winner = self.trick_forehand
        for i in range(1, len(self.cards)):
            if self.cards[i].card.beats(self.cards[self.cards.index(self.trick_winner)].card):
                self.trick_winner = self.cards[i].player

        self.logger.debug(f"Winner determined: {self.trick_winner}")

    def get_card_value_summary(self) -> str:
        return f"Total card value: {self.card_values}"

    def copy(self) -> 'Trick':
        trick_copy = Trick(self.trick_forehand)
        trick_copy.cards = self.cards[:]
        trick_copy.trick_winner = self.trick_winner
        trick_copy.card_values = self.card_values
        self.logger.debug(f"Trick copied: {trick_copy}")
        return trick_copy

    def __repr__(self) -> str:
        return (
            f"Trick(trick_forehand={self.trick_forehand}, "
            f"cards={self.cards}, card_values={self.card_values}, "
            f"trick_winner={self.trick_winner})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Trick):
            return False
        return (
            self.trick_forehand == other.trick_forehand and
            self.cards == other.cards and
            self.card_values == other.card_values and
            self.trick_winner == other.trick_winner
        )

    def __hash__(self) -> int:
        return hash((self.trick_forehand, tuple(self.cards), self.card_values, self.trick_winner))

    def reset_trick(self) -> None:
        self.cards.clear()
        self.card_values = 0
        self.trick_winner = None
        self.logger.info("Trick has been reset.")

    def get_trick_summary(self) -> str:
        card_strs = [f"{move.card} (Player: {move.player})" for move in self.cards]
        summary = (
            f"Trick summary:\n"
            f"Leading card: {self.leading_card}\n"
            f"Cards played: {', '.join(card_strs)}\n"
            f"Total card value: {self.card_values}\n"
            f"Trick winner: {self.trick_winner}\n"
        )
        return summary
