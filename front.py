import pygame
import sys
from back import Game

# Constants
BLUE = (20, 100, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)  # Bright Green for highlighting the active team score / active tile
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
CELL_THICKNESS = 1

# Colors for special tiles
SPECIAL_TILE_COLORS = {
                        '2L':(173, 216, 230), # Light Blue
                        '3L':(70, 130, 180), # Steel Blue
                        '2W':(255, 192, 203), # Pink
                        '3W':(204, 102, 153) # Steel Pink
                    }

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
    return textrect

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def align_text_and_rect(text, font, surface, rect):
    textobj = font.render(text, True, BLACK)
    textrect = textobj.get_rect(center=rect.center)
    surface.blit(textobj, textrect)
    return textrect

def draw_board(board, board_x, board_y, cell_size, surface, font, active_tile, placed_tiles):
    '''
    Draws the Scrabble board.
    '''
    for row in range(board.size):
        for col in range(board.size):
            cell = board.get_cell(row, col)
            rect = pygame.Rect(board_x + col * cell_size, board_y + row * cell_size, cell_size, cell_size)
            
            # Set color for special tiles
            if cell.bonus:
                color = SPECIAL_TILE_COLORS[cell.bonus]
            else:
                color = WHITE
            
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

            # Draw letter
            if cell.letter:
                draw_text(cell.letter, font, BLACK, surface, board_x + col * cell_size + cell_size // 2, board_y + row * cell_size + cell_size // 2)

            # Draw underline for blank tile
            if cell.blank:
                line_margin = cell_size // 4

                # Calculate underline position
                underline_start = (rect.left + line_margin, rect.bottom - line_margin)
                underline_end = (rect.right - line_margin, rect.bottom - line_margin)

                # Draw the underline
                pygame.draw.line(surface, BLACK, underline_start, underline_end, 4)

            # Highlight placed tiles
            if (row, col) in placed_tiles:
                pygame.draw.rect(surface, BLACK, rect, 3 * CELL_THICKNESS)

            # Highlight active tile
            if active_tile:
                active_row, active_col = active_tile
                if (active_row, active_col) == (row, col):
                    pygame.draw.rect(surface, HIGHLIGHT_COLOR, rect, 3 * CELL_THICKNESS)

def draw_team_scores(game, surface, font, team_x, team_y, spacing):
    '''
    Draw team scores.
    '''
    for i in range(len(game.scores)):
        team_text = f'Team {i+1}'
        text_y = team_y + i * spacing
        score_rect = pygame.Rect(team_x - BUTTON_WIDTH // 2, text_y + BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Highlight the current team's score
        if i == game.current_player:
            draw_rounded_rect(surface, HIGHLIGHT_COLOR, score_rect, 10)
        else:
            draw_rounded_rect(surface, WHITE, score_rect, 10)
        
        # Draw the team text
        draw_text(team_text, font, WHITE, surface, team_x, text_y)
        
        # Draw the score
        align_text_and_rect(str(game.scores[i]), font, surface, score_rect)

def draw_button(surface, font, rect, text):
    '''
    Draws a button (rectangle with text).
    '''
    draw_rounded_rect(surface, BLUE, rect, 10)
    draw_text(text, font, WHITE, surface, rect.centerx, rect.centery)

def draw_legend(surface, font, legend_x, legend_y, legend_spacing, cell_size):
    '''
    Draws a legend for special tile bonuses.
    '''
    for i, (text, color) in enumerate(SPECIAL_TILE_COLORS.items()):
        pygame.draw.rect(surface, color, (legend_x, legend_y + i * legend_spacing, cell_size, cell_size))
        draw_text(text, font, BLACK, surface, legend_x + cell_size // 2, legend_y + i * legend_spacing + cell_size // 2)

def game_screen(screen, WIDTH, HEIGHT, font, num_teams, board=None, scores=None, current_player=None, first_word_placed=False, loading=False):
    clock = pygame.time.Clock()
    game = None
    # Start a new game
    if not loading:
        game = Game(num_teams)
    # Load saved game
    else:
        game = Game(num_teams, board, scores, current_player, first_word_placed, loading=True)

    # Load dictionary
    game.load_dictionary('word_list.pkl')

    # Game board setup
    CELL_SIZE = HEIGHT // game.board.size

    # Calculate the board's top-left corner to center it horizontally
    board_x = WIDTH // 2 - (game.board.size * CELL_SIZE) // 2
    board_y = 0

    # Calculate spacing
    spacing = HEIGHT // 6  # Space between each team section

    # Calculate the center point between the left side of the screen and the board
    team_x = (board_x + 0) // 2
    team_y = HEIGHT // 6  # Starting y position for the first team section

    # Define the end turn button rectangle (bottom right)
    end_turn_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - 20, HEIGHT - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Define the quit button rectangle (top right)
    quit_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - 20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Define the legend
    legend_x = board_x + HEIGHT + team_x - (CELL_SIZE // 2)
    legend_y = (HEIGHT // 2) - (2 * CELL_SIZE)
    legend_spacing = 50

    # Define blank tile variables
    blank_tile_input = False
    blank_tile_text = ''
    blank_tile_pos = None
    
    while True:
        screen.fill(BLACK)  # Fill the screen with black

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if 'End Turn' button is clicked
                if end_turn_rect.collidepoint(mouse_x, mouse_y):
                    game.end_turn()
                # Check if 'Quit' button is clicked
                elif quit_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
                # Check if cell is clicked
                else:
                    col = (mouse_x - board_x) // CELL_SIZE
                    row = (mouse_y - board_y) // CELL_SIZE
                    if 0 <= row < game.board.size and 0 <= col < game.board.size and not game.board.get_cell(row, col).locked:
                        game.active_tile = (row, col)
            elif event.type == pygame.KEYDOWN and game.active_tile:
                row, col = game.active_tile
                # Check for letter deletion
                if event.key == pygame.K_BACKSPACE:
                    game.board.set_letter(row, col, '')
                    game.placed_tiles = [(r, c) for r, c in game.placed_tiles if (r, c) != (row, col)]
                # Check for blank tile use
                elif blank_tile_input:
                    if event.key == pygame.K_RETURN:
                        game.board.set_letter(blank_tile_pos[0], blank_tile_pos[1], blank_tile_text, blank=True)
                        blank_tile_input = False
                        blank_tile_text = ''
                        blank_tile_pos = None
                    else:
                        blank_tile_text = event.unicode.upper()
                # Check for letter tile use
                else:
                    char = event.unicode.upper()
                    if not game.board.get_cell(row, col).locked:
                        if char == '_':
                            blank_tile_input = True
                            blank_tile_pos = (row, col)
                        elif char.isalpha() and len(char) == 1:
                                game.board.set_letter(row, col, char)
                        if (row, col) not in game.placed_tiles:
                            game.placed_tiles.append((row, col))

        # Draw board
        draw_board(game.board, board_x, board_y, CELL_SIZE, screen, font, game.active_tile, game.placed_tiles)

        # Draw team scores
        draw_team_scores(game, screen, font, team_x,  team_y, spacing)

        # Draw 'End Turn' button
        draw_button(screen, font, end_turn_rect, 'END TURN')

        # Draw 'Quit' button
        draw_button(screen, font, quit_rect, 'QUIT')

        # Draw legend for special tiles
        draw_legend(screen, font, legend_x, legend_y, legend_spacing, CELL_SIZE)

        # Draw the input box for blank tile
        if blank_tile_input:
            pygame.draw.rect(screen, WHITE, (board_x + blank_tile_pos[1] * CELL_SIZE, board_y + blank_tile_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            draw_text(blank_tile_text, font, BLACK, screen, board_x + blank_tile_pos[1] * CELL_SIZE + CELL_SIZE // 2, board_y + blank_tile_pos[0] * CELL_SIZE + CELL_SIZE // 2)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
