# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input1.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. In this case, we're just converting strings to ints
depths = [int(line) for line in input_lines]

# Part 1: Count the number of times the depth increases from the previous values
increases = 0
for c in range(1, len(depths)):
	if depths[c] > depths[c-1]:
		increases += 1

print(f"Part 1: The number of increases was {increases}")

# Part 2: Do the same as above, but using three-sample averages.
increases = 0
for c in range(3, len(depths)):
	avg1 = depths[c-3] + depths[c-2] + depths[c-1]
	avg2 =               depths[c-2] + depths[c-1] + depths[c]
	if avg2 > avg1:
		increases += 1

print(f"Part 2: The number of increases was {increases}")
