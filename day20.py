# Read the input file. Ideally we would use a generator here, but then we'd have to keep the file
# handle alive.
with open('input20.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]
# Example20b.txt's answer is 5326

# Process the input. The first line is an image enhancement algorithm string. Next is a blank line
# followed by a 2D image. Both the algorithm and image are binary, consisting only of '.' and '#'.
enhancement_algorithm = input_lines[0]
input_image = [[c for c in row] for row in input_lines[2:]]

# Part 1: How many pixels are lit after running the enhancement algorithm twice? I have a feeling
# this is going to blow up in part 2, so I tried to use a sparse representation to avoid quadratic
# growth in processing and storage. Unfortunately, the lit pixels are pretty evently distributed in
# the active area, and for the actual input (but not the example!), algo[0] is lit, so the entire
# infinite field of pixels toggles on and off (!!). To get around this, I'll use an expanding window
# to track the active area and its immediate boundary.
class Field:
	def __init__(self, input_image, algo):
		self.rmin = -2
		self.cmin = -2
		self.rmax = len(input_image) + 1
		self.cmax = len(input_image[0]) + 1

		self.field = {}
		for r in range(self.rmin, self.rmax+1):
			for c in range(self.cmin, self.cmax+1):
				if r < 0 or c < 0 or r >= len(input_image) or c >= len(input_image[0]):
					self.field[(r, c)] = 0
				else:
					self.field[(r, c)] = 1 if input_image[r][c] == '#' else 0

		self.algo = [1 if c == '#' else 0 for c in algo]

	def __str__(self):
		s = []
		for r in range(self.rmin, self.rmax+1):
			for c in range(self.cmin, self.cmax+1):
				s.append('#' if self.field[(r, c)] else '.')
			s.append('\n')
		s.append(f"{self.rmin} {self.rmax} {self.cmin} {self.cmax}\n")
		return ''.join(s)

	def get_index_for_point(self, pr, pc):
		bin_num = 0
		for r in [pr-1, pr, pr+1]:
			for c in [pc-1, pc, pc+1]:
				bin_num = (bin_num << 1) + self.field[(r, c)]
		return bin_num

	def update_field(self):
		# Step 1: Calculate updates for all pixels including the inner boundary
		new_field = {}
		for r in range(self.rmin+1, self.rmax):
			for c in range(self.cmin+1, self.cmax):
				index = self.get_index_for_point(r, c)
				new_field[(r, c)] = self.algo[index]
		
		# Step 2: Change the outer boundary to the new background value
		# Step 3: Create a new outer boundary with values equal to the new inner boundary
		new_background = self.field[(self.rmin, self.cmin)] ^ self.algo[0]
		self.rmin -= 1
		self.cmin -= 1
		self.rmax += 1
		self.cmax += 1
		for r in [self.rmin, self.rmin+1, self.rmax-1, self.rmax]:
			for c in range(self.cmin, self.cmax+1):
				new_field[(r, c)] = new_background
		for c in [self.cmin, self.cmin+1, self.cmax-1, self.cmax]:
			for r in range(self.rmin+2, self.rmax-1):
				new_field[(r, c)] = new_background
		self.field = new_field
	
	def num_lit(self):
		return sum(self.field[(r, c)] for r in range(self.rmin+1, self.rmax) for c in range(self.cmin+1, self.cmax))

f = Field(input_image, enhancement_algorithm)
f.update_field()
f.update_field()
print(f"Part 1: The number of lit pixels after 2 iterations is {f.num_lit()}")

# Part 2: Enhance 50 times and count the number of lit pixels.
f = Field(input_image, enhancement_algorithm)
for _ in range(50):
	f.update_field()
print(f"Part 2: The number of lit pixels after 50 iterations is {f.num_lit()}")
