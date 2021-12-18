# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input15.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. It's a square grid of numerical risk levels.
input_risk_levels = [[int(col) for col in row] for row in input_lines]
grid_size = len(input_risk_levels)

# Part 1: Find the path from top-left to bottom-right with the lowest total risk and compute the risk.
class Position:
	def __init__(self, row, col, risk):
		self.risk = risk
		self.total_risk = 99999
		self.r = row
		self.c = col

	def __str__(self):
		return f'Pos({self.r}, {self.c}, {self.risk}, {self.total_risk})'

def create_grid(risk_levels, grid_size):
	grid = []
	for r in range(grid_size):
		grid.append([])
		for c in range(grid_size):
			grid[r].append(Position(r, c, risk_levels[r][c]))
	grid[0][0].total_risk = 0
	return grid

def copy_grid(grid):
	return [row[:] for row in grid]

def get_adjacent_coords(r, c, grid_size):
	coords = []
	if r > 0: coords.append((r-1, c))
	if c > 0: coords.append((r,   c-1))
	if r < grid_size - 1: coords.append((r+1, c))
	if c < grid_size - 1: coords.append((r,   c+1))
	return coords

def find_cheapest_paths(grid, grid_size):
	queue = [grid[0][0]]
	while len(queue) > 0:
		pos = queue.pop()
		for r, c in get_adjacent_coords(pos.r, pos.c, grid_size):
			new_total = pos.total_risk + grid[r][c].risk
			if new_total < grid[r][c].total_risk:
				grid[r][c].total_risk = new_total
				queue.insert(0, grid[r][c])

grid = create_grid(input_risk_levels, grid_size)
find_cheapest_paths(grid, grid_size)
print(f"Part 1: The total risk of the lowest-risk path is {grid[grid_size-1][grid_size-1].total_risk}")

# Part 2: The grid is five times larger. It repeats horizontally and vertically with each "tile"
# having all of its risk levels increased by one (with roll-over to zero).
new_grid_size = 5*grid_size
new_risk_levels = []
for r in range(new_grid_size):
	new_risk_levels.append([])
	for c in range(new_grid_size):
		base_risk = input_risk_levels[r % grid_size][c % grid_size]
		risk_adjust = (r // grid_size) + (c // grid_size)
		new_risk = base_risk + risk_adjust
		while new_risk >= 10:
			new_risk -= 9
		new_risk_levels[r].append(new_risk)

new_grid = create_grid(new_risk_levels, new_grid_size)
find_cheapest_paths(new_grid, new_grid_size)
print(f"Part 2: The total risk of the lowest-risk path is {new_grid[new_grid_size-1][new_grid_size-1].total_risk}")
