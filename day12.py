# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input12.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input, which is a list of pairwise connections between caves. Large caves are
# represented by capital letters and can be visited more than once. Small caves are represented
# by lowercase letters and can only be visited once.
caves = {}
for line in input_lines:
	cave1, cave2 = line.split('-')
	if cave1 not in caves:
		caves[cave1] = []
	if cave2 not in caves:
		caves[cave2] = []
	caves[cave1].append(cave2)
	caves[cave2].append(cave1)

# Part 1: Find the number of possible paths between the start and the end. Since the number of
# caves is small, a depth-first search using recursion seems like a decent place to start.
def find_path(cave, visited):
	if cave.islower() and cave not in visited:
		visited = visited.copy()
		visited.append(cave)
	for option in caves[cave]:
		if option not in visited:
			if option == 'end':
				global num_paths
				num_paths += 1
			else:
				find_path(option, visited)

num_paths = 0
find_path('start', [])
print(f"Part 1: The number of possible paths is {num_paths}")

# Part 2: Small caves may now be visited up to two times, except for the start and end caves.
def find_path2(cave, visited, twice):
	if cave.islower():
		if cave in visited:
			twice = True
		else:
			visited = visited.copy()
			visited.append(cave)
	for option in caves[cave]:
		if option.isupper() or option not in visited or not twice:
			if option == 'start':
				pass
			elif option == 'end':
				global num_paths
				num_paths += 1
			else:
				find_path2(option, visited, twice)

num_paths = 0
find_path2('start', [], False)
print(f"Part 2: The number of possible paths is {num_paths}")
