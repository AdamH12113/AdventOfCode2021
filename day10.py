# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input10.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# The input needs no processing
lines = input_lines

# Part 1: Find the first bad character in each corrupted lined and compute the total score.
scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
close_chars = {'(': ')', '[': ']', '{': '}', '<': '>'}

def find_bad_character(line):
	expected_close_chars = []
	for c in line:
		if c in close_chars.keys():
			expected_close_chars.append(close_chars[c])
		else:
			expected = expected_close_chars.pop()
			if c != expected:
				return c
	return None

total_score = 0
bad_chars = [find_bad_character(line) for line in lines]
total_score = sum(scores[bad_char] for bad_char in bad_chars if bad_char is not None)
print(f"Part 1: The total score is {total_score}")

# Part 2: Complete the incomplete lines
scores = {')': 1, ']': 2, '}': 3, '>': 4}
incomplete_lines = [line for line in lines if find_bad_character(line) is None]

def find_missing_characters(line):
	expected_close_chars = []
	for c in line:
		if c in close_chars.keys():
			expected_close_chars.append(close_chars[c])
		else:
			expected_close_chars.pop()
	expected_close_chars.reverse()
	return expected_close_chars

def score_missing_characters(missing_chars):
	score = 0
	for c in missing_chars:
		score = 5*score + scores[c]
	return score

line_scores = sorted([score_missing_characters(find_missing_characters(line)) for line in incomplete_lines])
median_score = line_scores[len(line_scores) // 2]
print(f"Part 2: The middle score is {median_score}")
