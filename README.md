# Scrabble Game

Welcome to the Scrabble Game! This application provides a digital interface to enhance your physical Scrabble playing experience. Here's a guide to help you get started.

### Code

- **App Download**: Download 'ScrabbleApp.exe'.
- **Python Files**: Backend code.
- **word_list.pkl**: Serialized dictionary.

## Features

- **Main Menu**: Navigate through the main menu with four buttons:
  - **New Game**: Start a new game.
  - **Load Game**: Load a saved game from `scrabble_game.json`.
  - **Rules**: View the rules, controls, and features of the app.
  - **Quit**: Exit the application.

- **New Game**: When you click the New Game button, you'll be taken to the teams screen to select the number of teams. You can also return to the main menu from this screen.

- **Load Game**: Load a previously saved game state from the `scrabble_game.json` file.

- **Rules**: Click this button to read about the rules, controls, and features of this application.

- **Quit**: Exit the application.

## Game Screen

When a game is started, you will see a digital board with the following elements:

- **Team Scores**: Displays the current scores of the teams.
- **Quit Button**: Exit the game and return to the main menu.
- **Legend for Tile Bonuses**: Shows the different tile bonuses available on the board.
- **End Turn Button**: Click this button to end your turn. This will check the placed tiles and update the board state.

### Using the Digital Board

The digital board is used alongside your physical Scrabble tiles to help calculate scores and validate words. Here's how to use it:

- **Placing Tiles**: Click on a cell to enter a letter. For blank tiles, enter '_' and you will be prompted to specify the letter. Press 'Enter' after typing the letter for your blank tile.
  - **Blank Tiles**: These will be underlined to indicate they are worth 0 points.
  - **Placed Tiles**: These will be outlined in BLACK.
  - **Active Tile**: This will be outlined in GREEN.

- **End Turn**: After clicking the End Turn button, the used bonuses will be removed both visually and internally, and the turn will end.

## Normal Scrabble Rules

This version of Scrabble adheres to the standard Scrabble rules, with the added functionality of a digital board for convenience.