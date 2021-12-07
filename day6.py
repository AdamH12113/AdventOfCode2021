# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input6.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]
example_input = ["3,4,3,1,2"]
#input_lines = example_input

# Process the input. There's one line consisting of a list of spawning dates for each lanternfish.
dates = [int(num) for num in input_lines[0].split(',')]

# Part 1: If lanternfish reproduce every 7 days, and newborn lanternfish need an extra 2 days to
# mature, how many laternfish would there be after 80 days? Since we only care about the age mod 9,
# we can track lanternfish counts in nine bins for efficiency. This will definitely come back to
# bite me in part 2 when the fish start dying or something.
bins = [0] * 9
for date in dates:
	bins[date] += 1

def age_fish(bins):
	num_spawning = bins[0]
	for b in range(1, 9):
		bins[b-1] = bins[b]
	bins[6] += num_spawning
	bins[8] = num_spawning

aged_bins = [b for b in bins]
for _ in range(80):
	age_fish(aged_bins)

num_fish = sum(aged_bins)
print(f"Part 1: After 80 days, there are {num_fish} lanternfish")

# Part 2: How many lanternfish would there be after 256 days? HA! My efficient implementation was
# the correct approach after all!
aged_bins = [b for b in bins]
for _ in range(256):
	age_fish(aged_bins)

num_fish = sum(aged_bins)
print(f"Part 2: After 256 days, there are {num_fish} lanternfish")
