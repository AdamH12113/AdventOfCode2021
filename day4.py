from colorama import init, Style, Fore
init()

# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input4.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. The first line is a set of call numbers separated by commas and followed by an
# empty line. After that, each bingo board is defined with five lines of five numbers each followed
# by an empty line.
call_nums = [int(num) for num in input_lines[0].split(',')]

board_values = []
for line in input_lines[1:]:
	if line == '':
		board_values.append([])
	else:
		board_values[-1].append([int(n) for n in line.split(' ') if n != ''])

class BingoBoard:
	def __init__(self, values):
		self.rows = values
		self.marked = [[False for _ in range(5)] for _ in range(5)]
		self.has_won = False
	
	def __str__(self):
		out = []
		for row in range(5):
			row_out = []
			for col in range(5):
				if self.marked[row][col]:
					row_out.append(f'{Style.BRIGHT}{Fore.GREEN}{self.rows[row][col]:2}{Fore.RESET}{Style.NORMAL}')
				else:
					row_out.append(f'{self.rows[row][col]:2}')
			out.append(' '.join(row_out))
		return '\n'.join(out)
	
	def mark(self, num):
		for row in range(5):
			for col in range(5):
				if self.rows[row][col] == num:
					self.marked[row][col] = True
		row_win = any(all(row) for row in self.marked)
		col_win = any(all(row[col] for row in self.marked) for col in range(5))
		self.has_won = row_win or col_win
	
	def unmarked_sum(self):
		return sum(sum(self.rows[row][col] for col in range(5) if not self.marked[row][col]) for row in range(5))
	
	def reset(self):
		self.marked = [[False for _ in range(5)] for _ in range(5)]
		self.has_won = False
			
	
boards = [BingoBoard(values) for values in board_values]

# Part 1: Determine which board will win first and calculate its score.
winner_found = False
for num in call_nums:
	for board in boards:
		board.mark(num)
		if board.has_won:
			print("WINNER!")
			print(board)
			winner_found = True
			score = board.unmarked_sum() * num
			print(f"Part 1: The score of the winning board was {score}\n")
			break
	if winner_found:
		break

# Part 2: Determine which board will win last and calculate its score.
for board in boards:
	board.reset()

for num in call_nums:
	active_boards = [board for board in boards if not board.has_won]
	for board in active_boards:
		board.mark(num)
		if len(active_boards) == 1 and board.has_won:
			print("LOSER!")
			print(board)
			score = board.unmarked_sum() * num
			print(f"Part 2: The score of the losing board was {score}")
