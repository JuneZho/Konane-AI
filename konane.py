'''
Game board class
'''
class Board:
	def __init__(self, width):
		self.width = width
		self.board = [[' ' for col in range(self.width + 1)] for row in range(self.width+1)]; #2D arr

	"initiate 8x8 board, 1 black, 0 white"
	def create_board(self, width):
		for row in range(self.width + 1):
			for col in range(self.width + 1):
				if(row == 0):
					self.board[row][col] = col;#put index
					self.board[row][0] = ' '

				elif(col == 0):
					self.board[row][col] = row

				elif((row + col) % 2 == 0):
					self.board[row][col] = '1'

				else:
					self.board[row][col] = '0'

		return self.board

	def print_board(self, board):
		for row in range(self.width + 1):
			for col in range(self.width + 1):
				print(board[row][col]),
			print


def start_game(width):
	board = Board(width)
	board.create_board(width)
	board.print_board(board.board)

start_game(8)
