import json
from front import game_screen
from back import Board
import os

def load_game(screen, WIDTH, HEIGHT, font):
    '''
    Loads a game from 'scrabble_game.json'.
    '''
    filename = 'scrabble_game.json'

    # if file doesn't exist in current directory, go back to main menu
    if not os.path.exists(filename):
        return
    
    with open(filename, 'r') as file:
        data = json.load(file)
        json_board = data['board']
        scores = data['scores']
        current_player = data['current_player']
        first_word_placed = data['first_word_placed']
        num_teams = len(scores)

        # Convert board back into a grid of cells
        board = Board()
        for row in range(board.size):
            for col in range(board.size):
                cell = json_board[row][col]
                board.set_cell(row, col, cell['letter'], cell['blank'], cell['locked'], cell['bonus'])

        # Load game screen
        game_screen(screen, WIDTH, HEIGHT, font, num_teams, board, scores, current_player, first_word_placed, loading=True)