# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input13.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. There's a list of coordinates of dots (one per line) followed by instructions
# for folding the paper.
coords = set()
folds = []
for line in input_lines:
	if ',' in line:
		coords.add(tuple(int(n) for n in line.split(',')))
	elif 'fold' in line:
		splits = line.split('=')
		axis = 0 if splits[0][-1] == 'x' else 1
		folds.append((axis, int(splits[1])))
	else:
		pass

def print_dots(coords):
	max_x = max(c[0] for c in coords)
	max_y = max(c[1] for c in coords)
	grid = [['.' for x in range(max_x + 1)] for y in range(max_y + 1)]
	for x, y in coords:
		grid[y][x] = '#'
	for y in range(max_y + 1):
		print(''.join(grid[y]))
	print()

# Part 1: How many dots are visible after completing the first fold?
def fold(coords, axis, location):
	below_fold = {c for c in coords if c[axis] > location}
	above_fold = coords - below_fold
	folded_dots = set()
	
	for c in below_fold:
		shift = c[axis] - location
		new_dot = [0, 0]
		new_dot[axis] = location - shift       # Overly-clever coordinate-independence
		new_dot[1 - axis] = c[1 - axis]        # with lists because tuples are immutable.
		folded_dots.add(tuple(new_dot))
	
	return above_fold | folded_dots

print(f"Part 1: The number of dots visible after the first fold is {len(fold(coords, *folds[0]))}")

# Part 2: Complete all of the folds to reveal eight capital letters. What are the letters? (We'll
# have to read them off the console because I'm not implementing OCR for this puzzle.)
for f in folds:
	coords = fold(coords, *f)
print("Part 2: The code is:")
print_dots(coords)
