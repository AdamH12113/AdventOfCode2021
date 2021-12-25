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
	print(player1.score, player2.score, d1, d2)

losing_score = player2.score if player1.won() else player1.score
print(f"Part 1: The product of the losing score and number of die rolls is {losing_score * die.num_rolls}")

# Part 2: Play the game again, this time with Dirac dice! Now we have to determine how many of the
# very, very large number of parallel universes are a win for each player.





