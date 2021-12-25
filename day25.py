# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input25.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. We have a 2D map consisting of sea cucumbers moving to the right, sea cucumbers
# moving down, and empty spaces.
input_map = [[col for col in row] for row in input_lines]

# Part 1: What is the first step on which no sea cucumbers move?
def step_map(current_map):
	num_rows = len(current_map)
	num_cols = len(current_map[0])
	moved = False

	new_map = [['.' for c in range(num_cols)] for r in range(num_rows)]
	for r in range(num_rows):
		for c in range(num_cols):
			if current_map[r][c] == '>':
				if current_map[r][(c+1) % num_cols] == '.':
					new_map[r][(c+1) % num_cols] = '>'
					moved = True
				else:
					new_map[r][c] = '>'
	for r in range(num_rows):
		for c in range(num_cols):
			if current_map[r][c] == 'v':
				if current_map[(r+1) % num_rows][c] != 'v' and new_map[(r+1) % num_rows][c] == '.':
					new_map[(r+1) % num_rows][c] = 'v'
					moved = True
				else:
					new_map[r][c] = 'v'
	return moved, new_map

cmap = [r[:] for r in input_map]
moved = True
step = 0
while moved:
	step += 1
	moved, cmap = step_map(cmap)
	if not moved:
		print(f"Part 1: The sea cucumbers stopped moving after {step} steps")
		break





