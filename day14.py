# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('example14.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. The first line is a polymer template. After an empty line, the remaining lines
# are a list of pair insertion rules.
template = input_lines[0]
rules = {line.split(' -> ')[0]: line.split(' -> ')[1] for line in input_lines[2:]}

# Part 1: After 10 pair insertion steps, what do you get if you subtract the quantity of the least
# common element from the quantity of the most common element?
def insert_pairs(polymer, rules):
	out_str = []
	for c in range(len(polymer) - 1):
		out_str.append(polymer[c])
		pair = polymer[c] + polymer[c+1]
		if pair in rules:
			out_str.append(rules[pair])
		else:
			print(skip)
	out_str.append(polymer[-1])
	return out_str

def count_elements(polymer):
	counts = {}
	for c in polymer:
		if c not in counts:
			counts[c] = 1
		else:
			counts[c] += 1
	return counts

polymer = template
for step in range(10):
	polymer = insert_pairs(polymer, rules)
counts = count_elements(polymer)
max_count = max(counts[e] for e in counts)
min_count = min(counts[e] for e in counts)
print(f"Part 1: The difference in quantities is {max_count} - {min_count} = {max_count - min_count}")

# Part 2: Now do 40 pair insertion steps. This cannot be brute-forced, so a different approach is
# needed. The rules cover every possible pair of elements, so one new element will be added between
# each pair in the polymer. The length of the polymer after each step is thus 2N - 1. That doesn't
# help us with the counts, though. Maybe a depth-first search would do better? No, we still have to
# go through the whole string of ~3 trillion elements. There must be some trick to it...
polymer = 'CH'
for step in range(10):
	polymer = insert_pairs(polymer, rules)
	print(step, ''.join(polymer))

exit()
counts = count_elements(polymer)
max_count = max(counts[e] for e in counts)
min_count = min(counts[e] for e in counts)
print(f"Part 2: The difference in quantities is {max_count} - {min_count} = {max_count - min_count}")
