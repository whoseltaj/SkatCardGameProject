import random
from game.skat.cards import Card


class Deck:
    def __init__(self):
        self.cards = self.create_deck()
        self.shuffle()

    @staticmethod
    def create_deck():
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        ranks = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        return [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_players):
        hands = [[] for _ in range(num_players)]
        for i, card in enumerate(self.cards):
            hands[i % num_players].append(card)
        return hands
