import os
import sys
import pygame
from game.skat.cardDeck import Deck

# Initialize Pygame
pygame.init()

# Configuration Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_SIZE = (80, 80)  # Player avatar size
CARD_SIZE = (110, 130)  # Card size
CARD_OFFSET_Y = 20

# Positions for players and table
PLAYER2_POSITION = (50, 100)
PLAYER3_POSITION = (WINDOW_WIDTH - 250, 100)
PLAYER1_POSITION = (WINDOW_WIDTH // 2 - PLAYER_SIZE[0] // 2, WINDOW_HEIGHT - PLAYER_SIZE[1] - 60)  # Middle bottom
TABLE_CENTER = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Initialize display and font
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Skat Card Game")
font = pygame.font.SysFont("timesnewroman", 13, bold=True)

# Player names and initial scores
PLAYER_NAMES = ["Player 2", "Player 3", "Me"]
PLAYER_SCORES = [0, 0, 0]  # Placeholder scores


# Load and scale images
def load_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)



current_dir = os.path.dirname(__file__)
table_image = load_image(os.path.join(current_dir, 'asserts/images/table/table.jpg'), WINDOW_SIZE)
player_images = [
    load_image(os.path.join(current_dir, f'asserts/images/players/pl{i + 1}.png'), PLAYER_SIZE) for i in range(3)
]
card_back_image = load_image(os.path.join(current_dir, 'asserts/images/cards/back_side.png'), CARD_SIZE)

# Initialize the card deck and deal cards
deck = Deck()
player_hands = deck.deal(3)


selected_card_index = None  # None means no card is currently selected


# Draw elements on the screen
def draw_background():
    screen.blit(table_image, (0, 0))


def draw_players():
    positions = [PLAYER2_POSITION, PLAYER3_POSITION, PLAYER1_POSITION]
    for i, pos in enumerate(positions):
        screen.blit(player_images[i], pos)
        draw_player_name_and_score(PLAYER_NAMES[i], PLAYER_SCORES[i], pos)


def draw_player_name_and_score(name, score, position):
    # Draw the player name
    name_text = font.render(name, True, WHITE)
    name_x = position[0] + (PLAYER_SIZE[0] - name_text.get_width()) // 2
    name_y = position[1] + PLAYER_SIZE[1]
    screen.blit(name_text, (name_x, name_y))

    # Draw the score text next to the player image
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_x = position[0] + PLAYER_SIZE[0] + 10
    score_y = position[1] + (PLAYER_SIZE[1] - score_text.get_height()) // 2
    screen.blit(score_text, (score_x, score_y))


def draw_player_cards():
    for i, hand in enumerate(player_hands):
        if i == 2:
            for j, card in enumerate(hand):
                card_image = pygame.transform.scale(card.image, CARD_SIZE)

                # Adjust position based on whether this specific card is selected
                left = PLAYER1_POSITION[0] + j * 35 - (len(hand) * 35 // 2)
                top = PLAYER1_POSITION[1] - CARD_SIZE[1] - 10
                if selected_card_index == j:
                    top -= CARD_OFFSET_Y

                screen.blit(card_image, (left, top))
        else:

            for j, card in enumerate(hand):
                left, top = calculate_card_position(i, j)
                screen.blit(card_back_image, (left, top))


def calculate_card_position(player_idx, card_idx):
    if player_idx == 0:

        left = PLAYER2_POSITION[0] + card_idx * 20
        top = PLAYER2_POSITION[1] + PLAYER_SIZE[1] + 30
    elif player_idx == 1:  #

        left = PLAYER3_POSITION[0] - card_idx * 20
        top = PLAYER3_POSITION[1] + PLAYER_SIZE[1] + 30
    return left, top


def draw_table_cards():

    top = 50
    for i in range(2):

        left = TABLE_CENTER[0] - CARD_SIZE[0] - 10 + i * (CARD_SIZE[0] + 20)
        screen.blit(card_back_image, (left, top))


def handle_card_click(pos):
    global selected_card_index

    for j in range(len(player_hands[2])):
        left = PLAYER1_POSITION[0] + j * 35 - (len(player_hands[2]) * 35 // 2)
        top = PLAYER1_POSITION[1] - CARD_SIZE[1] - 10


        if selected_card_index == j:
            top -= CARD_OFFSET_Y

        card_rect = pygame.Rect(left, top, CARD_SIZE[0], CARD_SIZE[1])


        if card_rect.collidepoint(pos):

            if selected_card_index == j:
                selected_card_index = None  
            else:
                selected_card_index = j  # Select this card
            break


# Main game loop
def main():
    try:
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    handle_card_click(event.pos)

            # Drawing sequence
            draw_background()
            draw_players()
            draw_player_cards()
            draw_table_cards()

            # Update display
            pygame.display.flip()

    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
