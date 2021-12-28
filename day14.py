# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input14.txt', 'rt') as f:
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
	return ''.join(out_str)

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
# go through the whole string of ~3 trillion elements. There must be some trick to it... A friend
# suggested keeping track of the count of each pair, which sounds reasonable.
def update_pair_counts(pair_counts, rules):
	new_counts = {pair: 0 for pair in rules}
	for pair in pair_counts:
		new_pair1 = pair[0] + rules[pair]
		new_pair2 = rules[pair] + pair[1]
		new_counts[new_pair1] += pair_counts[pair]
		new_counts[new_pair2] += pair_counts[pair]
	return new_counts

def get_element_list(pairs):
	elements = []
	for pair in rules:
		if pair[0] not in elements:
			elements.append(pair[0])
		if pair[1] not in elements:
			elements.append(pair[1])
	return ''.join(sorted(elements))

# Count the individual elements in the polymer based on the pair counts. Every element is double-
# counted since it's contained in the pairs on both sides, with the exception of the two elements
# on the ends of the string. One extra count is added for each of those elements to correct for the
# error when dividing.
def count_elements_in_pairs(pair_counts, template):
	element_counts = {e: 0 for e in get_element_list(pair_counts)}
	for pair in pair_counts:
		element_counts[pair[0]] += pair_counts[pair]
		element_counts[pair[1]] += pair_counts[pair]
	element_counts[template[0]] += 1
	element_counts[template[-1]] += 1
	return {e: element_counts[e]//2 for e in element_counts}


pair_counts = {pair: 0 for pair in rules}
for c in range(len(template) - 1):
	pair_counts[template[c:c+2]] += 1

for step in range(40):
	pair_counts = update_pair_counts(pair_counts, rules)

element_counts = count_elements_in_pairs(pair_counts, template)
max_count = max(element_counts.values())
min_count = min(element_counts.values())
print(f"Part 2: The difference in quantities is {max_count} - {min_count} = {max_count - min_count}")
