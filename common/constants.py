from enum import Enum


FPS = 60

# Cards
SUITS = ['Clubs', 'Hearts', 'Spades', 'Diamonds']
RANKS = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']


# Actions
class Actions(Enum):
    DRAW = '1'
    DRAW_HIDDEN = '2'
    DECLARE_GAME = '3'
    BID = '4'
    PLAY_CARD = '5'
    PASS = '6'
    ANNOUNCE = '7'
    VIEW_HAND = '8'
    VIEW_TABLE = '9'
    VIEW_SCORES = '10'
