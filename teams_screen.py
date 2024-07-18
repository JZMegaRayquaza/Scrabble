import pygame
import sys
from front import game_screen

# Constants
BLUE = (20, 100, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_HEIGHT = 60
BUTTON_MARGIN = 20
BUTTON_WIDTH = 240

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
    return textrect

def teams_screen(screen, WIDTH, HEIGHT, font):
    clock = pygame.time.Clock()

    # Calculate button positions before the main loop
    title_x = WIDTH // 2
    title_y = HEIGHT // 6
    button_texts = ['2', '3', '4']
    button_x_positions = [
        WIDTH // 2 - BUTTON_WIDTH - BUTTON_MARGIN,
        WIDTH // 2,
        WIDTH // 2 + BUTTON_WIDTH + BUTTON_MARGIN,
    ]
    buttons = [
        pygame.Rect(button_x_positions[i] - BUTTON_WIDTH // 2, title_y + 50, BUTTON_WIDTH, BUTTON_HEIGHT)
        for i in range(len(button_texts))
    ]

    # Return to main menu rectangle and text
    return_button_text = 'Return to Main Menu'
    button_text_rect = draw_text(return_button_text, font, WHITE, screen, WIDTH // 2, HEIGHT - BUTTON_HEIGHT // 2 - 20)
    return_button_width = button_text_rect.width + 40  # Add padding around the text
    return_button = pygame.Rect((WIDTH - return_button_width) // 2, HEIGHT - BUTTON_HEIGHT - 20, return_button_width, BUTTON_HEIGHT)

    # Set a time delay for user interaction with buttons (2 seconds)
    pygame.time.set_timer(pygame.USEREVENT, 2000)
    buttons_enabled = False

    while True:
        screen.fill(BLACK)  # Fill the screen with black

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                buttons_enabled = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons_enabled:
                mouse_x, mouse_y = event.pos

                # Check if 'Return to Main Menu' button is clicked
                if return_button.collidepoint(mouse_x, mouse_y):
                    return  # Return to main menu

                # Check if one of the team buttons is clicked
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_x, mouse_y):
                        game_screen(screen, WIDTH, HEIGHT, font, i + 2)  # start game with number of teams

        draw_text('How many teams?', font, WHITE, screen, title_x, title_y)

        # Draw team buttons
        for i, text in enumerate(button_texts):
            button = buttons[i]
            pygame.draw.rect(screen, BLUE, button)
            draw_text(text, font, WHITE, screen, button.centerx, button.centery)

        # Draw 'Return to Main Menu' button
        pygame.draw.rect(screen, BLUE, return_button)
        draw_text(return_button_text, font, WHITE, screen, return_button.centerx, return_button.centery)

        # Update the display
        pygame.display.flip()
        clock.tick(60)
