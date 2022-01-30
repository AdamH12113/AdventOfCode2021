import copy

# The input is too simple to bother with parsing a file.
example_positions = (4, 8)
input_positions = (7, 8)
starting_positions = example_positions

# Part 1: Play a practice game. What is the product of the losing player's score and the number of
# times the die was rolled?
class DeterministicDie:
	def __init__(self):
		self.next_value = 1
		self.num_rolls = 0
	
	def roll(self):
		result = self.next_value
		self.next_value += 1
		if self.next_value > 100:
			self.next_value = 1
		self.num_rolls += 1
		return result

class Pawn:
	def __init__(self, starting_position, shared_die):
		self.pos = starting_position
		self.score = 0
		self.die = shared_die
	
	def take_turn(self):
		die_roll = self.die.roll() + self.die.roll() + self.die.roll()
		self.pos += die_roll
		while self.pos > 10:
			self.pos -= 10
		self.score += self.pos
		return self.pos

	def won(self):
		return self.score >= 1000

die = DeterministicDie()
player1 = Pawn(starting_positions[0], die)
player2 = Pawn(starting_positions[1], die)
while True:
	d1 = player1.take_turn()
	if player1.won():
		break
	d2 = player2.take_turn()
	if player2.won():
		break

losing_score = player2.score if player1.won() else player1.score
print(f"Part 1: The product of the losing score and number of die rolls is {losing_score * die.num_rolls}")

# Part 2: Play the game again, this time with Dirac dice! Now we have to determine how many of the
# very, very large number of parallel universes are a win for each player. We'll count positions
# starting from zero here to make things easier.
start_state = {'position': [starting_positions[0], starting_positions[1]], 'score': [0, 0], 'turn': 0}
known_wins = {}

def make_updated_state(state, roll):
	turn = state['turn']
	new_state = copy.deepcopy(state)
	new_state['position'][turn] = (state['position'][turn] + roll) % 10
	new_state['score'][turn] += new_state['position'][turn] + 1
	new_state['turn'] = 1 - turn
	return new_state

def state_key(s):
	return (s['position'][0], s['position'][1], s['score'][0], s['score'][1], s['turn'])

def check_win_cache(state):
	key = state_key(state)
	if key in known_wins:
		return known_wins[key]
	else:
		return None
	

def count_wins(state, depth):
	cache_key = state_key(state)
	if cache_key in known_wins:
		print('Cache:', known_wins[cache_key])
		return known_wins[cache_key]

	wins = [0, 0]
	for roll in (1, 2, 3):
		new_state = make_updated_state(state, roll)
		print(roll, state_key(new_state))
		if new_state['score'][0] >= 21:
			print('Win 1', depth)
			wins[0] += 1
		elif new_state['score'][1] >= 21:
			print('Win 2', depth)
			wins[1] += 1
		else:
			new_wins = count_wins(new_state, depth + 1)
			wins[0] += new_wins[0]
			wins[1] += new_wins[1]
	result = tuple(wins)
	known_wins[cache_key] = result
	return result

final_wins = count_wins(start_state, 0)
print(final_wins)
		




