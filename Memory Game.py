import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CARD_WIDTH, CARD_HEIGHT = 100, 100
PADDING = 10
GRID_COLS, GRID_ROWS = 4, 4
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 60)
BLUE = (0, 123, 255)
GREEN = (40, 167, 69)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
cards = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H']
random.shuffle(cards)  # Shuffle the card values

first_card = None
second_card = None
flipped_cards = []
lock_board = False
matches_found = 0

# Helper function to create a grid of cards
def create_card_grid():
    """Creates the grid of cards with shuffled values."""
    grid = []
    for row in range(GRID_ROWS):
        grid_row = []
        for col in range(GRID_COLS):
            card_value = cards[row * GRID_COLS + col]
            card_rect = pygame.Rect(
                col * (CARD_WIDTH + PADDING) + PADDING,
                row * (CARD_HEIGHT + PADDING) + PADDING,
                CARD_WIDTH, CARD_HEIGHT
            )
            grid_row.append({'rect': card_rect, 'value': card_value, 'flipped': False})
        grid.append(grid_row)
    return grid

# Function to draw a single card
def draw_card(card, flipped=False):
    """Draws a card on the screen, flipped or hidden based on its state."""
    rect = card['rect']
    if flipped:
        pygame.draw.rect(SCREEN, GREEN, rect)
        text = FONT.render(card['value'], True, WHITE)
        SCREEN.blit(text, (rect.x + (CARD_WIDTH - text.get_width()) // 2, 
                           rect.y + (CARD_HEIGHT - text.get_height()) // 2))
    else:
        pygame.draw.rect(SCREEN, BLUE, rect)

# Function to check if two selected cards match
def check_for_match():
    """Checks if the two selected cards match."""
    global first_card, second_card, lock_board, matches_found

    if first_card['value'] == second_card['value']:
        # Cards match, leave them flipped
        first_card['flipped'] = True
        second_card['flipped'] = True
        matches_found += 1
    else:
        # Cards don't match, flip them back after a short delay
        pygame.time.wait(1000)  # 1 second delay for visual effect
        first_card['flipped'] = False
        second_card['flipped'] = False
    
    # Reset selection and unlock the board
    first_card = None
    second_card = None
    lock_board = False

# Main game loop
def game_loop():
    global first_card, second_card, lock_board

    running = True
    card_grid = create_card_grid()

    while running:
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not lock_board:
                pos = pygame.mouse.get_pos()

                # Check which card is clicked
                for row in card_grid:
                    for card in row:
                        if card['rect'].collidepoint(pos) and not card['flipped']:
                            if not first_card:
                                # Flip first card
                                first_card = card
                                card['flipped'] = True
                            elif not second_card:
                                # Flip second card and lock the board for checking
                                second_card = card
                                card['flipped'] = True
                                lock_board = True
                                check_for_match()  # Check for a match immediately after flipping

        # Draw all cards on the grid
        for row in card_grid:
            for card in row:
                draw_card(card, flipped=card['flipped'])

        # Update the display
        pygame.display.flip()

        # Check if the player has found all matches
        if matches_found == len(cards) // 2:
            print("You win!")
            time.sleep(2)
            running = False  # Exit the game loop when all matches are found

    pygame.quit()

# Start the game
game_loop()
