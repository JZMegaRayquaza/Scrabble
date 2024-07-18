import pygame
import sys
from rules_screen import rules_screen
from teams_screen import teams_screen
from load_game import load_game

# Initialize pygame
pygame.init()

# Constants
BLUE = (20, 100, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BUTTON_HEIGHT = 60
BUTTON_MARGIN = 20

# Create screen in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Scrabble')

# Get screen dimensions
WIDTH, HEIGHT = screen.get_size()
FONT_SIZE = TILE_SIZE = HEIGHT // 15

# Load font
font = pygame.font.Font(None, FONT_SIZE)

def draw_text(text, font, color, surface, x, y):
    '''
    Draw text centered at (x, y).
    '''
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
    return textrect

def draw_title(title):
    '''
    Draws the title 'SCRABBLE' in Scrabble tiles.
    '''
    total_width = len(title) * (TILE_SIZE + 5) - 5
    start_x = (WIDTH - total_width) // 2
    y = 100
    for i, letter in enumerate(title):
        pygame.draw.rect(screen, BLUE, (start_x + i * (TILE_SIZE + 5), y, TILE_SIZE, TILE_SIZE))
        draw_text(letter, font, WHITE, screen, start_x + i * (TILE_SIZE + 5) + TILE_SIZE // 2, y + TILE_SIZE // 2)

def draw_buttons(buttons, max_button_width):
    '''
    Draw buttons for main menu.
    '''
    start_y = HEIGHT // 2
    for i, button in enumerate(buttons):
        x = (WIDTH - max_button_width) // 2
        y = start_y + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
        pygame.draw.rect(screen, BLUE, (x, y, max_button_width, BUTTON_HEIGHT))
        draw_text(button, font, WHITE, screen, x + max_button_width // 2, y + BUTTON_HEIGHT // 2)

def main_menu():
    clock = pygame.time.Clock()

    buttons = ["NEW GAME", "LOAD GAME", "RULES", "QUIT"]
    button_widths = [font.size(button)[0] + 40 for button in buttons]
    max_button_width = max(button_widths)

    while True:
        screen.fill(BLACK)  # Fill the screen with black

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for i, button in enumerate(buttons):
                    x = (WIDTH - max_button_width) // 2
                    y = HEIGHT // 2 + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
                    if x <= mouse_x <= x + max_button_width and y <= mouse_y <= y + BUTTON_HEIGHT:
                        if button == "NEW GAME":
                            teams_screen(screen, WIDTH, HEIGHT, font)
                        elif button == "LOAD GAME":
                            load_game(screen, WIDTH, HEIGHT, font)
                        elif button == "RULES":
                            rules_screen(screen, WIDTH, HEIGHT, font)
                        elif button == "QUIT":
                            pygame.quit()
                            sys.exit()

        # Draw title
        draw_title('SCRABBLE')

        # Draw buttons
        draw_buttons(buttons, max_button_width)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main_menu()
