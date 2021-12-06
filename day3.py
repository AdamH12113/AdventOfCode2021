# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input3.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. Each line is a 12-bit binary number. As an embedded programmer, it pains me to
# work with binary numbers in this inefficient way, but it is actually easier for both parts. :-(
bit_depth = len(input_lines[0])
input_nums = [[int(b) for b in bstr] for bstr in input_lines]

# Part 1: Find the most common bit in each position, then multiply the resulting binary number and
# its inverse.
def most_common_bit(nums, bit_pos, least_common = False):
	total = sum(num[bit_pos] for num in nums)
	if total == len(nums)/2:
		return 0 if least_common else 1
	mcb = round(total / len(nums))
	return (1 - mcb) if least_common else mcb

def invert(num):
	return [1 - num[bit] for bit in range(len(num))]

def bin_to_dec(num):
	total = 0
	for bit in num:
		total = (total << 1) + bit
	return total

gamma_rate = [most_common_bit(input_nums, bit) for bit in range(bit_depth)]
epsilon_rate = invert(gamma_rate)
product = bin_to_dec(gamma_rate) * bin_to_dec(epsilon_rate)
print(f"Part 1: The gamma rate is {gamma_rate}, the epsilon rate is {epsilon_rate}, and their product is {product}")

# Part 2: Filter the numbers by looking at the most common value in each bit position, then keeping
# the numbers with that value in that position. Repeat for each bit position. Then do the same for
# the least common values.
def filter_by_bit(nums, bit_pos, least_common = False):
	mcb = most_common_bit(nums, bit_pos, least_common)
	return [n for n in nums if n[bit_pos] == mcb]

def filter_to_one(nums, least_common = False):
	new_nums = nums
	for bit in range(bit_depth):
		new_nums = filter_by_bit(new_nums, bit, least_common)
		if len(new_nums) == 1:
			break
	return new_nums[0]

oxygen_rating = filter_to_one(input_nums)
co2_rating = filter_to_one(input_nums, True)
product = bin_to_dec(oxygen_rating) * bin_to_dec(co2_rating)

print(f"Part 2: The oxygen rating is {oxygen_rating}, the CO2 rating is {co2_rating}, and their product is {product}")
