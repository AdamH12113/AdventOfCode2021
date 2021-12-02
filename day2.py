import numpy as np

# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input2.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. Each line gives us either a change in horizontal position
# or a change in vertical position. NumPy is a big overkill, but it makes working
# with vectors so easy.
forward = np.array([1, 0])
down = np.array([0, 1])
course = []
for line in input_lines:
	try:
		direction, magnitude = line.split(' ')
		if direction == 'forward':
			course.append(int(magnitude) * forward)
		elif direction == 'down':
			course.append(int(magnitude) * down)
		else:
			course.append(-int(magnitude) * down)
	except Exception as e:
		print("Format error in line:", line)
		print(e)
		exit()

# Part 1: Compute the product of the horizontal and vertical position after following
# the course.
h, v = sum(course)
print(f"Part 1: The new position is ({h}, {v}) with product {h * v}")

# Part 2: Keep track of a hidden third variable, "aim".
h = 0
v = 0
aim = 0
for instruction in course:
	h += instruction[0]
	v += aim * instruction[0]
	aim += instruction[1]
print(f"Part 2: The new position is ({h}, {v}) with product {h * v}")

