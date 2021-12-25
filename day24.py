# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input24.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# The input will be processed at run time.

# Part 1: Implement the ALU and run the provided program to find the largest valid 14-digit model
# number that does not contain zeros.
class ALU:
	def __init__(self):
		self.ops = {'inp': self.inp, 'add': self.add, 'mul': self.mul, 'div': self.div, 'mod': self.mod, 'eql': self.eql}
		self.reset()
	
	def reset(self):
		self.vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0, 'imm': 0}
		self.input = []

	def __str__(self):
		return f"ALU {self.vars['w']}, {self.vars['x']}, {self.vars['y']}, {self.vars['z']} {self.input}"
	
	def inp(self, a):
		#self.vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0, 'imm': 0}
		self.vars['z'] = self.prev_z
		self.vars[a] = self.input.pop(0)
	def add(self, a, b):
		self.vars[a] += self.vars[b]
	def mul(self, a, b):
		self.vars[a] *= self.vars[b]
	def div(self, a, b):
		self.vars[a] = self.vars[a] // self.vars[b]
	def mod(self, a, b):
		self.vars[a] = self.vars[a] % self.vars[b]
	def eql(self, a, b):
		self.vars[a] = int(self.vars[a] == self.vars[b])

	def run(self, program, input):
		self.reset()
		self.input = list(input)
		for instruction in program:
			parts = instruction.split(' ')
			if len(parts) == 3 and (parts[2][0] == '-' or parts[2].isnumeric()):
				self.vars['imm'] = int(parts[2])
				parts[2] = 'imm'
			self.ops[parts[0]](*parts[1:])

# This is too slow to run directly, but luckily there's another dirty trick in this puzzle --
# the validity of each digit is computed separately in the Y register right before the next inp
# instruction. So by looking at the Y register for each digit, we can check nine numbers instead
# of 100 trillion.
alu = ALU()
for model_num in range(1, 9+1, 1):
	for prev_z in range(0, 26+1):
		alu.prev_z = prev_z
		model_str = f"{model_num:014}"
		print(f"{model_num} {prev_z}: ", end='')
		alu.run(input_lines, map(int, model_str))
		print(alu.vars['z'])

alu.run(input_lines, map(int, str(13579246899999)))
print(alu.vars['z'])





