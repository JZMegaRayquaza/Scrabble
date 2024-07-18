import pickle
import json

# Letter values
LETTER_VALUES = {
	'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
	'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
	'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
	'Y': 4, 'Z': 10
}

class Cell:
	def __init__(self, letter=None, blank=False, locked=False, bonus=None):
		self.letter = letter
		self.blank = blank
		self.locked = locked
		self.bonus = bonus

class Board:
	def __init__(self, size=15):
		self.size = size
		self.grid = [[Cell() for _ in range(size)] for _ in range(size)]
		self.initialize_special_tiles()

	def get_cell(self, row, col):
		return self.grid[row][col]

	def set_cell(self, row, col, letter, blank=False, locked=False, bonus=None):
		cell = self.grid[row][col]
		cell.letter = letter
		cell.blank = blank
		cell.locked = locked
		cell.bonus = bonus

	def set_letter(self, row, col, letter, blank=False):
		cell = self.grid[row][col]
		cell.letter = letter
		cell.blank = blank

	def set_locked(self, row, col, locked=True):
		cell = self.grid[row][col]
		cell.locked = locked

	def set_bonus(self, row, col, bonus=None):
		cell = self.grid[row][col]
		cell.bonus = bonus

	def initialize_special_tiles(self):
		'''
		Define special tiles.
		'''
		special_tiles = {
			(0, 0): '3W', (0, 7): '3W', (0, 14): '3W',
			(7, 0): '3W', (7, 14): '3W', (14, 0): '3W',
			(14, 7): '3W', (14, 14): '3W',

			(1, 1): '2W', (2, 2): '2W', (3, 3): '2W',
			(4, 4): '2W', (7, 7): '2W', (10, 10): '2W', 
			(11, 11): '2W', (12, 12): '2W', (13, 13): '2W',

			(1, 13): '2W', (2, 12): '2W', (3, 11): '2W',
			(4, 10): '2W', (10, 4): '2W', (11, 3): '2W',
			(12, 2): '2W', (13, 1): '2W',

			(5, 1): '3L', (9, 1): '3L', (5, 5): '3L',
			(9, 5): '3L', (1, 5): '3L', (13, 5): '3L',
			(5, 9): '3L', (9, 9): '3L', (1, 9): '3L',
			(13, 9): '3L', (5, 13): '3L', (9, 13): '3L',

			(3, 0): '2L', (11, 0): '2L', (6, 2): '2L',
			(8, 2): '2L', (0, 3): '2L', (7, 3): '2L',
			(14, 3): '2L', (2, 6): '2L', (6, 6): '2L',
			(8, 6): '2L', (12, 6): '2L', (3, 7): '2L',
			(11, 7): '2L', (2, 8): '2L', (6, 8): '2L',
			(8, 8): '2L', (12, 8): '2L', (0, 11): '2L',
			(7, 11): '2L', (14, 11): '2L', (6, 12): '2L',
			(8, 12): '2L', (3, 14): '2L', (11, 14): '2L',
		}

		for (row, col), bonus in special_tiles.items():
			self.grid[row][col].bonus = bonus

class Game:
	def __init__(self, num_teams, board=None, scores=None, current_player=None, first_word_placed=False, loading=False):
		if loading:
			# Load the saved game state
			self.board = board
			self.scores = scores
			self.current_player = current_player
		else:
			# Set up a new game
			self.board = Board()
			self.scores = [0] * num_teams
			self.current_player = 0
		
		# Needed for proper game state
		self.first_word_placed = first_word_placed
		
		self.dictionary = set()
		self.placed_tiles = []
		self.active_tile = None
		self.main_word_tiles = []
		self.secondary_word_tiles = []

	def load_dictionary(self, file_path):
		'''
		Loads a serialized word list.
		'''
		with open(file_path, 'rb') as file:
			self.dictionary = pickle.load(file)

	def save_game(self, filename='scrabble_game.json'):
		'''
		Saves Scrabble board, scores, current player, and 
		whether the first word has been placed into a json.
		'''
		# Convert board to serializable format
		board = []
		for row in range(self.board.size):
			board.append([])
			for col in range(self.board.size):
				cell = self.board.grid[row][col]
				board[-1].append({'letter': cell.letter, 'blank': cell.blank, 'locked': cell.locked, 'bonus': cell.bonus})

		# Dump game state into json
		with open(filename, 'w') as file:
			json.dump({
				'board': board,
				'scores': self.scores,
				'current_player': self.current_player,
				'first_word_placed': self.first_word_placed
			}, file, indent=4)

	def end_turn(self):
		'''
		Checks if played tiles are valid:
			1. Remove tiles if invalid move.
			2. Updates score, and locks tiles if valid move.
			3. Moves on to next team.
		'''
		if not self.first_word_placed:
			if not self.check_first_turn_valid() or not self.check_word_valid():
				self.remove_placed_tiles()
				self.next_turn()
				return
			self.first_word_placed = True
		elif not self.check_word_valid():
			self.remove_placed_tiles()
			self.next_turn()
			return
		self.update_score()
		self.lock_placed_tiles()
		self.next_turn()

	def check_first_turn_valid(self):
		'''
		Check if the first word goes through the center of the board.
		'''
		for row, col in self.placed_tiles:
			if row == 7 and col == 7:
				return True
		return False

	def check_one_line(self):
		'''
		Check if placed tiles are only in one row or column.
		'''
		rows = [tile[0] for tile in self.placed_tiles]
		cols = [tile[1] for tile in self.placed_tiles]
		return len(set(rows)) == 1 or len(set(cols)) == 1

	def check_too_many_tiles(self):
		'''
		Check if more than 7 tiles are played.
		'''
		return len(self.placed_tiles) > 7

	def check_consecutive(self):
		'''
		Check if the placed tiles form a consecutive sequence in the row or column.
		'''
		rows = sorted(set(tile[0] for tile in self.placed_tiles))
		cols = sorted(set(tile[1] for tile in self.placed_tiles))

		if len(rows) == 1:
			# Single row, check if columns form a consecutive sequence
			for i in range(cols[0], cols[-1]):
				cell = self.board.get_cell(rows[0], i)
				next_cell = self.board.get_cell(rows[0], i+1)
				if not(cell.letter and next_cell.letter):
					return False
		elif len(cols) == 1:
			# Single column, check if rows form a consecutive sequence
			for i in range(rows[0], rows[-1]):
				cell = self.board.get_cell(i, cols[0])
				next_cell = self.board.get_cell(i+1, cols[0])
				if not(cell.letter and next_cell.letter):
					return False

		return True

	def check_word_connected(self):
		'''
		Check if the word is connected to any existing tiles on the board.
		'''
		if self.first_word_placed:
			for row, col in self.placed_tiles:
				if self.is_connected(row, col):
					return True
			return False

		# For the first word, it must pass through the center
		return self.check_first_turn_valid()

	def is_connected(self, row, col):
		'''
		Check if the given tile position is connected to an existing tile.
		'''
		directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
		for dr, dc in directions:
			r, c = row + dr, col + dc
			if 0 <= r < 15 and 0 <= c < 15 and self.board.get_cell(r, c).locked:
				return True
		return False

	def check_in_dictionary(self):
		'''
		Checks if played tiles form words in the dictionary.
		'''
		words = []

		# Get main word
		main_word = ''.join([tile.letter for tile in self.main_word_tiles])
		words.append(main_word)

		# Get secondary words
		for tile_list in self.secondary_word_tiles:
			secondary_word = ''.join([tile.letter for tile in tile_list])
			words.append(secondary_word)

		for word in words:
			if word:
				if word not in self.dictionary:
					return False
				
		# Main word and all secondary words are valid        
		return True


	def check_word_valid(self):
		'''
		Checks if a word is valid by validating the following:
			1. Uses 7 or fewer tiles.
			2. Tiles are only in 1 row or column.
			3. Tiles form a continuous sequence.
			4. The word is connected to existing tiles.
			5. In the dictionary.
		'''
		if self.check_too_many_tiles() or not self.check_one_line():
			return False

		if not self.first_word_placed and not self.check_first_turn_valid():
			return False

		if not self.check_word_connected():
			return False
		
		if not self.check_consecutive():
			return False
		
		horizontal = self.get_main_word()
		self.get_secondary_words(horizontal)

		if not self.check_in_dictionary():
			return False

		return True
	
	def get_main_word(self):
		'''
		Get the main word formed by the placed tile(s) and existing tiles,
		along with its orientation as a boolean (horizontal=True, vertical=False).
		'''
		if len(self.placed_tiles) > 1:
			self.placed_tiles.sort()
			rows = [tile[0] for tile in self.placed_tiles]
			cols = [tile[1] for tile in self.placed_tiles]

			# horizontal word
			if len(set(rows)) == 1:
				word = self.get_row_word(rows, cols)
				self.main_word_tiles = word
				return True
			# vertical word
			elif len(set(cols)) == 1:
				word = self.get_col_word(rows, cols)
				self.main_word_tiles = word
				return False
		
		elif len(self.placed_tiles) == 1:
			row, col = self.placed_tiles[0]

			# Check horizontally
			row_word = self.get_row_word([row], [col])

			# Check vertically
			col_word = self.get_col_word([row], [col])

			# If there's a word in both directions, choose the longer one
			if row_word and col_word:
				if len(row_word) > len(col_word):
					self.main_word_tiles = row_word
					return True
				else:
					self.main_word_tiles = col_word
					return False
			elif row_word:
				self.main_word_tiles = row_word
				return True
			elif col_word:
				self.main_word_tiles = col_word
				return False

		# No word
		return None

	def get_secondary_words(self, main_word_orientation):
		'''
		Get all secondary words formed by placed tiles.
		'''
		# Horizontal main word
		if main_word_orientation:
			for row, col in self.placed_tiles:
				col_word = self.get_col_word([row], [col])
				if len(col_word) > 1:
					self.secondary_word_tiles.append(col_word)
		# Vertical main word
		else:
			for row, col in self.placed_tiles:
				row_word = self.get_row_word([row], [col])
				if len(row_word) > 1:
					self.secondary_word_tiles.append(row_word)

	def get_row_word(self, rows, cols):
		'''
		Get horizontal word.
		'''
		word = []

		# Find the leftmost tile
		left_col = cols[0]
		while left_col > 0 and self.board.get_cell(rows[0], left_col - 1).letter:
			left_col -= 1

		# Find the rightmost tile
		right_col = cols[-1]
		while right_col < self.board.size - 1 and self.board.get_cell(rows[0], right_col + 1).letter:
			right_col += 1

		# Get main word
		for col in range(left_col, right_col + 1):
			cell = self.board.get_cell(rows[0], col)
			word.append(cell)
		
		return word
	
	def get_col_word(self, rows, cols):
		'''
		Get vertical word.
		'''
		word = []

		# Find the topmost tile
		top_row = rows[0]
		while top_row > 0 and self.board.get_cell(top_row - 1, cols[0]).letter:
			top_row -= 1

		# Find the bottommost tile
		bottom_row = rows[-1]
		while bottom_row < self.board.size - 1 and self.board.get_cell(bottom_row + 1, cols[0]).letter:
			bottom_row += 1

		# Get main word
		for row in range(top_row, bottom_row + 1):
			cell = self.board.get_cell(row, cols[0])
			word.append(cell)

		return word

	def remove_placed_tiles(self):
		'''
		Removed placed tiles if invalid move.
		'''
		for row, col in self.placed_tiles:
			self.board.set_letter(row, col, '')

	def lock_placed_tiles(self):
		'''
		Lock placed tiles if valid move. Tiles can't be changed after placed.
		'''
		for row, col in self.placed_tiles:
			self.board.set_locked(row, col)
			self.board.set_bonus(row, col)

	def next_turn(self):
		'''
		Increase turn counter and reset previous tiles.
		'''
		self.current_player = (self.current_player + 1) % len(self.scores)
		self.active_tile = None
		self.placed_tiles.clear()
		self.main_word_tiles.clear()
		self.secondary_word_tiles.clear()
		self.save_game()

	def update_score(self):
		'''
		Update score based on placed tiles.
		'''
		score = 0
		word_multiplier = 1

		# Calculate score for main word
		for cell in self.main_word_tiles:
			if not cell.blank and cell.letter in LETTER_VALUES:
				letter_value = LETTER_VALUES[cell.letter]
				if cell.bonus == '2L':
					score += 2 * letter_value
				elif cell.bonus == '3L':
					score += 3 * letter_value
				else:
					score += letter_value
			if cell.bonus == '2W':
				word_multiplier *= 2
			elif cell.bonus == '3W':
				word_multiplier *= 3
		self.scores[self.current_player] += (score * word_multiplier)

		# Calculate score for secondary words
		for cell_list in self.secondary_word_tiles:
			secondary_score = 0
			secondary_word_multiplier = 1
			for cell in cell_list:
				if not cell.blank and cell.letter in LETTER_VALUES:
					letter_value = LETTER_VALUES[cell.letter]
					if cell.bonus == '2L':
						secondary_score += 2 * letter_value
					elif cell.bonus == '3L':
						secondary_score += 3 * letter_value
					else:
						secondary_score += letter_value
				if cell.bonus == '2W':
					secondary_word_multiplier *= 2
				elif cell.bonus == '3W':
					secondary_word_multiplier *= 3
			self.scores[self.current_player] += (secondary_score * secondary_word_multiplier)

		# 50 pt bonus
		if len(self.placed_tiles) == 7:
			self.scores[self.current_player] += 50