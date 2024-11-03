import pygame

class Card:
    value = None
    suit = None
    image = None
    rect = None
    points = None

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(f'asserts/images/cards/{rank}_{suit.lower()}.png').convert()
        self.rect = None
        self.points = self.calculate_points()

    def calculate_points(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        elif self.rank == '10':
            return 10
        else:
            return 0

    def set_rect(self, rect):
        # Adjust the width to make only one card clickable in the hand
        left, top, width, height = rect
        self.rect = pygame.Rect(left, top, 25, height)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
