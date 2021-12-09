# Read the input file. Ideally we would use a generator here, but then we'd have to keep the file
# handle alive.
with open('input8.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. Each line contains ten unique signal patterns representing the ten scrambled
# digits, as well as four signal patterns representing the current state of a four-digit display.
unique_pattern_sets = [[sorted(pattern) for pattern in line.split(' | ')[0].split(' ')] for line in input_lines]
output_value_sets = [[sorted(value) for value in line.split(' | ')[1].split(' ')] for line in input_lines]

# Part 1: How many output values are 1, 4, 7, or 8? Each of these has a unique number of signals.
#   1: 2
#   4: 4
#   7: 3
#   8: 7
# I'm in a bad mood so I'm going to do this with an overly-complicated one-liner.
total = sum(1 for output_values in output_value_sets for val in output_values if len(val) == 2 or len(val) == 4 or len(val) == 3 or len(val) == 7 )
print(f"Part 1: The digits 1, 4, 7, and 8 appear {total} times")

# Part 2: Decode the output values using the unique signal patterns. The number of signals for each
# digit are:
#   0: 6
#   1: 2
#   2: 5
#   3: 5
#   4: 4
#   5: 5
#   6: 6
#   7: 3
#   8: 7
#   9: 6
# The five-digit numbers are 2, 3, and 5, and the six-digit numbers are 0, 6, and 9.
def decode_mapping(unique_patterns):
	# The shared segments between the digits impose constraints on this problem. Using these, we can
	# identify the five-digit and six-digit numbers.
	#   4 & 2 = two signals
	#   1 & 3 = 1
	#   5 is the remaining five-digit number
	#   4 & 9 = 4
	#   7 & 6 = two signals
	#   0 is the remaining six-digit number
	sigsets = {}
	sigsets[1] = set(next(p for p in unique_patterns if len(p) == 2))
	sigsets[4] = set(next(p for p in unique_patterns if len(p) == 4))
	sigsets[7] = set(next(p for p in unique_patterns if len(p) == 3))
	sigsets[8] = set(next(p for p in unique_patterns if len(p) == 7))

	five_digit_sets = [p for p in unique_patterns if len(p) == 5]
	for signals in five_digit_sets:
		if len(sigsets[4].intersection(signals)) == 2:
			sigsets[2] = set(signals)
		elif sigsets[1].intersection(signals) == sigsets[1]:
			sigsets[3] = set(signals)
		else:
			sigsets[5] = set(signals)
	
	six_digit_sets = [p for p in unique_patterns if len(p) == 6]
	for signals in six_digit_sets:
		if sigsets[4].intersection(signals) == sigsets[4]:
			sigsets[9] = set(signals)
		elif len(sigsets[7].intersection(signals)) == 2:
			sigsets[6] = set(signals)
		else:
			sigsets[0] = set(signals)
	
	# Now that we have the input signal sets for each number, we need to find the corresponding
	# output signal mappings. We can take the intersection of every input signal set where an output
	# signal must appear, and the only value should be the corresponding input.
	out_uses = {'a': [0,2,3,5,6,7,8,9], 'b': [0,4,5,6,8,9], 'c': [0,1,2,3,4,7,8,9],
	            'd': [2,3,4,5,6,8,9], 'e': [0,2,6,8], 'f': [0,1,3,4,5,6,7,8,9], 'g': [0,2,3,5,6,8,9]}
	out_to_in_map = {}
	for output in 'abcdefg':
		options = set('abcdefg')
		for number in range(10):
			if number in out_uses[output]:
				options = options.intersection(sigsets[number])
			else:
				options -= sigsets[number]
		out_to_in_map[output] = options.pop()
	in_to_out_map = {v: k for k, v in out_to_in_map.items()}
	return in_to_out_map

def decode_digit(map, input_signals):
	num_map = {'abcefg': 0, 'cf': 1, 'acdeg': 2, 'acdfg': 3, 'bcdf': 4, 'abdfg': 5, 'abdefg': 6, 'acf': 7, 'abcdefg': 8, 'abcdfg': 9}
	sig_str = ''.join(sorted(map[x] for x in input_signals))
	return num_map[sig_str]

def decode_outputs(map, output_signal_sets):
	sum = 0
	for s in output_signal_sets:
		num = decode_digit(map, s)
		sum = 10*sum + num
	return sum

checksum = 0
for display in range(len(unique_pattern_sets)):
	dmap = decode_mapping(unique_pattern_sets[display])
	out_val = decode_outputs(dmap, output_value_sets[display])
	checksum += out_val
print(f"Part 2: The sum of the output values is {checksum}")
