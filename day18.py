import json

# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input18.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. Each line is a snailfish number, a set of recursive pairs of integers. We need
# to turn the strings into nested lists and then process those into a recursive data structure. Since
# the nested lists also happen to be valid JSON strings, we can use the built-in JSON module to do
# the parsing for us.
input_nested_lists = [json.loads(line) for line in input_lines]

class SnailfishNumber:
	def __init__(self, nested_list, parent=None, side='root', depth=0):
		self.parent = parent
		self.side = side
		self.depth = depth
		if type(nested_list[0]) is int:
			self.left = nested_list[0]
		else:
			self.left = SnailfishNumber(nested_list[0], self, 'left', depth + 1)
		if type(nested_list[1]) is int:
			self.right = nested_list[1]
		else:
			self.right = SnailfishNumber(nested_list[1], self, 'right', depth + 1)
	
	def __str__(self):
		start_str = f"{self.depth * '  '}{self.side}\n"
		left_str = f"{self.depth * '  '}  {self.left}\n" if type(self.left) is int else str(self.left)
		right_str = f"{self.depth * '  '}  {self.right}\n" if type(self.right) is int else str(self.right)
		return start_str + left_str + right_str
	
	def explode(self):
		# Go up until we find a node with a left branch. This is the nearest common ancester of the
		# regular number immediately to the left in the nsted list.
		node = self
		while node.side == 'left':
			node = node.parent
		
		if node.side != 'root':
			# The closest regular number may be a direct child of the common ancestor
			node = node.parent
			if type(node.left) is int:
				node.left += self.left
			else:
				# Go left, then go down the right branches until we reach the bottom. This is the closest
				# regular number on the left side.
				node = node.left
				while type(node.right) is not int:
					node = node.right
				node.right += self.left
		
		# Now repeat for the nearest number on the right
		node = self
		while node.side == 'right':
			node = node.parent
		
		if node.side != 'root':
			node = node.parent
			if type(node.right) is int:
				node.right += self.right
			else:
				node = node.right
				while type(node.left) is not int:
					node = node.left
				node.left += self.right
		
		# Replace the exploding pair with zero
		if self.side == 'left':
			self.parent.left = 0
		else:
			self.parent.right = 0
	
	# Check whether this node should explode. If so, do it. If not, try the child nodes. Only one
	# node should explode.
	def explode_step(self):
		if self.depth >= 4 and type(self.left) is int and type(self.right) is int:
			self.explode()
			return True
		
		return ((type(self.left) is SnailfishNumber and self.left.explode_step()) or
		        (type(self.right) is SnailfishNumber and self.right.explode_step()))
	
	# If a child is a regular number greater than or equal to ten, split it into a pair. Only one
	# number should split.
	def split_step(self):
		if type(self.left) is int and self.left >= 10:
			self.left = SnailfishNumber([self.left // 2, (self.left+1) // 2], self, 'left', self.depth + 1)
			return True
		if type(self.left) is SnailfishNumber and self.left.split_step():
			return True
			
		if type(self.right) is int and self.right >= 10:
			self.right = SnailfishNumber([self.right // 2, (self.right+1) // 2], self, 'right', self.depth + 1)
			return True
		if type(self.right) is SnailfishNumber and self.right.split_step():
			return True
		return False
	
	# Revert to nested list form for easier addition
	def to_nested_list(self):
		left = self.left if type(self.left) is int else self.left.to_nested_list()
		right = self.right if type(self.right) is int else self.right.to_nested_list()
		return [left, right]
	
	# Add and reduce
	def __add__(self, other):
		new_sn = SnailfishNumber([self.to_nested_list(), other.to_nested_list()])
		while new_sn.explode_step() or new_sn.split_step():
			pass
		return new_sn

	# Score for puzzle purposes
	def magnitude(self):
		left_mag = self.left if type(self.left) is int else self.left.magnitude()
		right_mag = self.right if type(self.right) is int else self.right.magnitude()
		return 3*left_mag + 2*right_mag

# Part 1: Find the magnitude of the sum of all numbers in the input list.
sum = SnailfishNumber(input_nested_lists[0])
for n in range(1, len(input_nested_lists)):
	sum = sum + SnailfishNumber(input_nested_lists[n])
print(f"Part 1: The magnitude of the sum of the input numbers is {sum.magnitude()}")

# Part 2: What is the largest magnitude we can get from adding only two numbers? Note that addition
# is non-commutative here.
max_mag = 0
nums = [SnailfishNumber(n) for n in input_nested_lists]
for n1 in range(len(nums)):
	for n2 in range(len(nums)):
		if n1 == n2:
			continue
		mag = (nums[n1] + nums[n2]).magnitude()
		max_mag = max(max_mag, mag)
print(f"Part 2: The maximum magnitude attainable from adding two numbers is {max_mag}")
