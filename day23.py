# Process the input. It's too simple to bother with files. We just have a list of which amphipods are
# in which rooms.
# D C B C
# D A A B


# Part 1: What is the least energy required to organize the amphipods into the correct room? This
# is basically a Tower of Hanoi puzzle, but with different costs for moving the "discs". It was
# easier to solve this by hand than write a program for it. The answer is 19059 with the following
# movement costs:
#     20 B in third room up and right
#      8 A in third room to the top left
#    500 C in second room to its home
#      5 A in second room to the top left
#     50 B in hallway to its home
#    400 C in fourth room to its home
#     70 B in fourth room to its home
#   9000 D in first room to its home
#   9000 D in first room to its home
#      3 A in top left to its home
#      3 A in top left to its home
# -----------------------------------------------
#  19059 Total

# Part 2: Now there are 16 amphipods and the rooms are four spaces deep. No way we're doing this by
# hand!
# D C B C
# D A A B
input = 'DDACABBC'
input = 'DDDDDABCCAABBBCAC'
example = 'ADDBDBCCCABBACAD'
movement_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

class Amphipod:
	# Valid states are wrong_room, hallway, and right_room
	def __init__(self, letter, state='wrong_room'):
		self.letter = letter
		self.state = state

class Hallway:
	def __init__(self, order):
		self.rooms = {'A': [order[0], order[1]], 'B': [order[2], order[3]], 'C': [order[4], order[5]], 'D': [order[6], order[7]]}
		self.left = []
		self.right = []
		self.AB = None
		self.BC = None
		self.CD = None
		self.lowest_cost = 999999
	
	def get_valid_moves(self):
		

# 19071 too high
D 9 9
C 5 4
B 4 3 7
A 6 7 9 9
18000 + 900 + 140 + 31

D               9M9M
C     5M    4M
B 2H      5M  7M
A   8L  5L          3M3M




