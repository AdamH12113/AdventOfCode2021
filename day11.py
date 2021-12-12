from colorama import init, Style, Fore
init()

# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input11.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input, which is just a 10x10 grid of numbers.
starting_energies = [[int(col) for col in row] for row in input_lines]
grid_size = len(starting_energies[0])

# Part 1: Determine the total number of flashes after 100 time steps.
class OctopusGrid:
	def __init__(self, energies, grid_size):
		self.energies = [row[:] for row in energies]
		self.flashed = [[False for col in row] for row in energies]
		self.grid_size = grid_size
	
	# Get the adjacent coordinates for a given location, taking edges into account
	def adjacent(self, r, c):
		coords = []
		for dr in [-1, 0, 1]:
			for dc in [-1, 0, 1]:
				if r+dr >= 0 and r+dr < self.grid_size and c+dc >= 0 and c+dc < self.grid_size and not (dr == 0 and dc == 0):
					coords.append((r+dr, c+dc))
		return coords
	
	def increment_all_energies(self):
		self.energies = [[self.energies[r][c] + 1 for c in range(self.grid_size)] for r in range(self.grid_size)]
	
	def increment_adjacent_energies(self, row, col):
		for (r, c) in self.adjacent(row, col):
			self.energies[r][c] += 1
	
	def flash(self, row, col):
		if self.flashed[row][col] or self.energies[row][col] <= 9:
			return False
		self.flashed[row][col] = True
		self.increment_adjacent_energies(row, col)
		return True
	
	def flash_all(self):
		check_needed = True
		num_flashes = 0
		while check_needed:
			check_needed = False
			for r in range(self.grid_size):
				for c in range(self.grid_size):
					if self.flash(r, c):
						check_needed = True
						num_flashes += 1
		return num_flashes

	def relax_energies(self):
		for r in range(self.grid_size):
			for c in range(self.grid_size):
				if self.flashed[r][c]:
					self.energies[r][c] = 0
		self.flashed = [[False for col in row] for row in self.energies]
	
	def all_flashed(self):
		return all(all(row) for row in self.flashed)

	def step(self):
		self.increment_all_energies()
		num_flashes = self.flash_all()
		sync = self.all_flashed()
		self.relax_energies()
		return num_flashes, sync

	def __str__(self):
		out = []
		for r in range(self.grid_size):
			for c in range(self.grid_size):
				if self.flashed[r][c]:
					out.append(f"{Style.BRIGHT}{Fore.YELLOW}")
				else:
					out.append(f"{Style.NORMAL}{Fore.RESET}")
				out.append(f"{self.energies[r][c]:>3}")
			out.append('\n')
		out.append(f"{Style.NORMAL}{Fore.RESET}")
		return ''.join(out)

grid = OctopusGrid(starting_energies, grid_size)
num_flashes = 0
for s in range(100):
	num_flashes += grid.step()[0]
print(f"Part 1: There were {num_flashes} flashes")

# Part 2: Find the first step where all octopuses flash at the same time.
grid = OctopusGrid(starting_energies, grid_size)
step = 0
while True:
	step += 1
	synced = grid.step()[1]
	if synced:
		print(f"Part 2: All octopuses flashed at step {step}")
		break
