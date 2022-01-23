import copy

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

class Room:
	def __init__(self, letter, depth):
		self.letter = letter
		self.spaces = [None] * depth
	
	def __str__(self):
		return f'{self.letter} {self.spaces} {self.can_pop()} {self.done()}'

	def fill(self, letters):
		for s in range(len(letters)):
			self.spaces[len(self.spaces) - (s + 1)] = letters[s]

	def can_pop(self):
		return any((space and space != self.letter) for space in self.spaces)
	
	def can_push(self, letter):
		has_space = not all(self.spaces)
		valid_letter = (letter == self.letter and not self.can_pop()) or self.letter not in list('ABCD')
		return has_space and valid_letter

	# Return the topmost amphipod in the room along with the base cost of getting it out
	def pop(self):
		if self.can_pop():
			for s in range(len(self.spaces)):
				if self.spaces[s]:
					val = self.spaces[s]
					self.spaces[s] = None
					return val, s + 1
		else:
			raise IndexError(f'Tried to pop empty room {self.letter}: {self.spaces}')
	
	# Push the amphipod into the lowest space in the room and return the base cost of moving it in
	def push(self, letter):
		depth = len(self.spaces)
		if self.can_push(letter):
			for s in range(depth):
				if self.spaces[depth - (s+1)] is None:
					self.spaces[depth - (s+1)] = letter
					return depth - (s+1) + 1
		else:
			raise IndexError(f'Tried to push into full/invalid room {self.letter}: {letter} {self.spaces}')
	
	def top(self):
		for s in range(len(self.spaces)):
			if self.spaces[s]:
				return self.spaces[s]
		return None
	
	def empty(self):
		return not any(self.spaces)
	
	def done(self):
		if self.letter in list('ABCD') and all(space == self.letter for space in self.spaces):
			return True
		else:
			return not any(self.spaces)

class Hallway:
	movement_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
	room_list = ['L', 'A', 'AB', 'B', 'BC', 'C', 'CD', 'D', 'R']
	home_list = ['A', 'B', 'C', 'D']
	extra_costs = {
		'L':  {'L': 0, 'A': 0, 'AB': 0, 'B': 2, 'BC': 2, 'C': 4, 'CD': 4, 'D': 6, 'R': 6},
		'A':  {'L': 0, 'A': 0, 'AB': 0, 'B': 2, 'BC': 2, 'C': 4, 'CD': 4, 'D': 6, 'R': 6},
		'AB': {'L': 0, 'A': 0, 'AB': 0, 'B': 0, 'BC': 0, 'C': 2, 'CD': 2, 'D': 4, 'R': 4},
		'B':  {'L': 2, 'A': 2, 'AB': 0, 'B': 0, 'BC': 0, 'C': 2, 'CD': 2, 'D': 4, 'R': 4},
		'BC': {'L': 2, 'A': 2, 'AB': 0, 'B': 0, 'BC': 0, 'C': 0, 'CD': 0, 'D': 2, 'R': 2},
		'C':  {'L': 4, 'A': 4, 'AB': 2, 'B': 2, 'BC': 0, 'C': 0, 'CD': 0, 'D': 2, 'R': 2},
		'CD': {'L': 4, 'A': 4, 'AB': 2, 'B': 2, 'BC': 0, 'C': 0, 'CD': 0, 'D': 0, 'R': 0},
		'D':  {'L': 6, 'A': 6, 'AB': 4, 'B': 4, 'BC': 2, 'C': 2, 'CD': 0, 'D': 0, 'R': 0},
		'R':  {'L': 6, 'A': 6, 'AB': 4, 'B': 4, 'BC': 2, 'C': 2, 'CD': 0, 'D': 0, 'R': 0}
	}
	
	# To keep this small, each blocking point has a list of rooms to its left and a list of rooms to
	# its right. If the source and destination rooms are in different groups, a block is possible.
	blocks = {
		'AB': [['L', 'A'], ['B', 'BC', 'C', 'CD', 'D', 'R']],
		'BC': [['L', 'A', 'AB', 'B'], ['C', 'CD', 'D', 'R']],
		'CD': [['L', 'A', 'AB', 'B', 'BC', 'C'], ['D', 'R']],
	}

	def __init__(self, room_depth, fills):
		self.rooms = {
			'L': Room('L', 2),
			'A': Room('A', room_depth),
			'AB': Room('AB', 1),
			'B': Room('B', room_depth),
			'BC': Room('BC', 1),
			'C': Room('C', room_depth),
			'CD': Room('CD', 1),
			'D': Room('D', room_depth),
			'R': Room('R', 2)
		}
		for room in 'ABCD':
			self.rooms[room].fill(fills[:room_depth])
			fills = fills[room_depth:]
	
	def __str__(self):
		s = []
		for room in self.rooms:
			s.append(str(self.rooms[room]))
		return '\n'.join(s)
	
	def done(self):
		return all(room.done() for room in self.rooms.values())
	
	def can_move(self, src, dest):
		if src == dest or (src not in Hallway.home_list and dest not in Hallway.home_list):
			return False
		pod = self.rooms[src].top()
		if not (self.rooms[src].can_pop() and self.rooms[dest].can_push(pod)):
			return False
		for chokepoint in Hallway.blocks:
			left = Hallway.blocks[chokepoint][0]
			right = Hallway.blocks[chokepoint][1]
			if ((src in left and dest in right) or (src in right and dest in left)) and not self.rooms[chokepoint].empty():
				return False
		return True
	
	def move(self, src, dest):
		if self.can_move(src, dest):
			cost = 0
			pod, cost = self.rooms[src].pop()
			cost += Hallway.extra_costs[src][dest]
			cost += self.rooms[dest].push(pod)
			return cost * Hallway.movement_costs[pod]
		else:
			raise IndexError(f"Can't move from {src} to {dest}:\n{self.rooms[src]}\n{self.rooms[dest]}")
	
	# This is kind of a cheat. It only works if it's possible to move all of the D amphipods
	# directly from their current location to their home. Doing this greatly prunes the search
	# space, but doesn't work for all possible inputs.
	def get_valid_moves(self):
		move_list = []
		for room1 in Hallway.room_list:
			pod = self.rooms[room1].top()
			if pod and self.can_move(room1, pod):
				move_list.append((room1, pod))
			elif pod != 'D':
				for room2 in Hallway.room_list:
					if self.can_move(room1, room2):
						move_list.append((room1, room2))
		return move_list

lowest_cost = 999999
def find_cheapest_solution(hallway, cost):
	global lowest_cost
	if cost >= lowest_cost:
		return
	if hallway.done():
		print(f"Done {cost}")
		lowest_cost = cost
		return

	valid_moves = hallway.get_valid_moves()
	for src, dest in valid_moves:
		if cost >= lowest_cost:
			return
		new_hallway = copy.deepcopy(hallway)
		new_cost = cost + new_hallway.move(src, dest)
		find_cheapest_solution(new_hallway, new_cost)

example1 = 'ABDCCBAD'
example2 = 'ADDBDBCCCABBACAD'
input1 = 'DDACABBC'
input2 = 'DDDDABCCAABBBCAC'
room_list = ['L', 'A', 'AB', 'B', 'BC', 'C', 'CD', 'D', 'R']
hw = Hallway(4, input2)
find_cheapest_solution(hw, 0)
print(f"Part 2: The lowest possible cost is {lowest_cost}")
