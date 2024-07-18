import pygame
import sys

# Constants
BLUE = (20, 100, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_HEIGHT = 60

# List of rules text for multiple pages
RULES_TEXT = [
    # page 1 (setup)
    [
        "SETUP",
        "1. Form 2 to 4 teams.",
        "2. Each team draws 7 tiles from the bag without looking."
    ],
    # page 2 (objective)
    [
        "OBJECTIVE",
        "1. Score more points than other teams.",
        "2. Points are scored by placing words on the game board."
    ],
    # page 3 (board)
    [
        "BOARD",
        "1. A standard Scrabble board consists of cells located in a 15x15 grid.",
        "2. Letter tiles are placed in these cells."
    ],
    # page 4 (tiles)
    [
        "TILES",
        "- There are 100 tiles.",
        "- E (x12)",
        "- A, I (x9)",
        "- O (x8)",
        "- M, R, T (x6)",
        "- L, S, U, D (x4)",
        "- G (x3)",
        "- B, C, M, P, F, H, V, W, Y, _ (x2)",
        "- K, J, X, Q, Z (x1)"
    ],
    # page 5 (blank tile)
    [
        "BLANK TILE",
        "1. Blank tiles can be used as any letter.",
        "2. When a blank is played, it will remain the letter it was played as."
    ],
    # page 6 (tile values)
    [
        "TILE VALUES",
        "0 pts: _",
        "1 pt: A, E, I, L, N, O, R, S, T, U",
        "2 pts: D, G",
        "3 pts: B, C, M, P",
        "4 pts: F, H, V, W, Y",
        "5 pts: K",
        "8 pts: J, X",
        "10 pts: Q, Z"
    ],
    # page 7 (special cells)
    [
        "SPECIAL CELLS",
        "Center: The starting word must go through the center of the board.",
        "2L: Light blue cells double the value of the tile placed on that cell.",
        "3L: Steel blue cells triple the value of the tile placed on that cell.",
        "2W: Light pink cells double the value of the word placed thru that cell.",
        "3W: Steel pink cells triple the value of the word placed thru that cell.",
        "",
        "Note: These extra point cells can only be used ONCE."
    ],
    # page 8 (taking a turn)
    [
        "TAKING A TURN",
        "Option 1: Place a word.",
        "Option 2: Exchange for new tiles.",
        "Option 3: Pass.",
        "",
        'Note: Play continues clockwise.'
    ],
    # page 9 (replacing tiles)
    [
        "REPLACING TILES",
        "Once tiles are played, teams will draw tiles until they have 7."
    ],
    # page 10 (50 pt bonus)
    [
        "50 POINT BONUS",
        "A team receives an extra 50 points when using all 7 tiles."
    ],
    # page 11 (the end)
    [
        "THE END",
        "Once all tiles are gone from the bag and",
        "a team has used all their tiles, the game ends."
    ],
    # page 12 (dictionary)
    [
        "DICTIONARY",
        "This version of Scrabble uses a dictionary from redbo's GitHub repository."
    ],
    # page 13 (controls)
    [
        "CONTROLS",
        "1. Click on a cell and enter a letter.",
        "2. If a tile is blank, enter '_'. This will prompt you to enter a letter.",
        "3. Click the 'End turn' button after you played a word, exchanged, or passed."
    ],
    # page 14 (features)
    [
        "FEATURES",
        "1. Active tile will be highlighted in GREEN.",
        "2. Placed tiles will be highlighted in BLACK."
    ],
    # page 15 (autosave)
    [
        "AUTOSAVE",
        "After every turn, the game will automatically be saved to a '.json' file.",
        "When 'LOAD GAME' is clicked, it will load 'scrabble_game.json'."
    ]
]

def draw_text(text, font, color, surface, x, y, align='topleft'):
    textobj = font.render(text, True, color)
    if align == 'topleft':
        textrect = textobj.get_rect(topleft=(x, y))
    if align == 'center':
        textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
    return textrect

def draw_rules(current_page, font, surface):
    '''
    Draw the rules for the current page.
    '''
    for i, line in enumerate(RULES_TEXT[current_page]):
        draw_text(line, font, WHITE, surface, 50, 100 + i * 50)

def draw_arrows(surface, arrow_height, width):
    '''
    Draw left and right arrow for navigating rules.
    '''
    # Draw left arrow
    left_arrow = [(50, arrow_height), (100, arrow_height - 25), (100, arrow_height + 25)]
    pygame.draw.polygon(surface, BLUE, left_arrow)
    
    # Draw right arrow
    right_arrow = [(width - 50, arrow_height), (width - 100, arrow_height - 25), (width - 100, arrow_height + 25)]
    pygame.draw.polygon(surface, BLUE, right_arrow)

def rules_screen(screen, WIDTH, HEIGHT, font):
    clock = pygame.time.Clock()

    total_pages = len(RULES_TEXT)
    current_page = 0

    # Return to main menu rectangle and text
    return_button_text = 'Return to Main Menu'
    button_text_rect = draw_text(return_button_text, font, WHITE, screen, WIDTH // 2, HEIGHT - BUTTON_HEIGHT // 2 - 20)
    return_button_width = button_text_rect.width + 40  # Add padding around the text
    return_button = pygame.Rect((WIDTH - return_button_width) // 2, HEIGHT - BUTTON_HEIGHT - 20, return_button_width, BUTTON_HEIGHT)

    while True:
        screen.fill(BLACK)  # Fill the screen with black

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                # Check if 'Return to Main Menu' button is clicked
                if return_button.collidepoint(mouse_x, mouse_y):
                    return  # Return to main menu
                # Check if left arrow is clicked
                if 50 <= mouse_x <= 100 and ARROW_HEIGHT - 25 <= mouse_y <= ARROW_HEIGHT + 25:
                    if current_page > 0:
                        current_page -= 1
                # Check if right arrow is clicked
                if WIDTH - 100 <= mouse_x <= WIDTH - 50 and ARROW_HEIGHT - 25 <= mouse_y <= ARROW_HEIGHT + 25:
                    if current_page < total_pages - 1:
                        current_page += 1

        # Draw current rules text
        draw_rules(current_page, font, screen)

        # Draw arrows
        ARROW_HEIGHT = (3 * HEIGHT // 4)
        draw_arrows(screen, ARROW_HEIGHT, WIDTH)
        
        # Draw page number
        page_number = f'{current_page + 1}/{total_pages}'
        draw_text(page_number, font, WHITE, screen, WIDTH // 2, ARROW_HEIGHT)

        # Draw 'Return to Main Menu' button
        pygame.draw.rect(screen, BLUE, return_button)
        draw_text(return_button_text, font, WHITE, screen, return_button.centerx, return_button.centery, align='center')

        # Update the display
        pygame.display.flip()
        clock.tick(60)
