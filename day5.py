import re

# Read the input file. Ideally we would use a generator here, but then we'd have to keep the file
# handle alive.
with open('input5.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. Each line consists of a set of two points defining a line segment. Python
# doesn't have a built-in equivalent to scanf(), but regexes are the next-best thing. I found a
# neat algorithm that tests for line intersection, so I'm going to plan to use that just for fun.
# https://stackoverflow.com/a/565282/5220760
class Vector:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)
	
	def __str__(self):
		return f"{self.x:>4},{self.y:>4}"
	
	def __add__(self, v2):
		return Vector(self.x + v2.x, self.y + v2.y)
	
	def __sub__(self, v2):
		return Vector(self.x - v2.x, self.y - v2.y)
	
	def cross(self, v2):
		return (self.x * v2.y) - (self.y * v2.x)

class Line:
	def __init__(self, x1, y1, x2, y2):
		self.p1 = Vector(x1, y1)
		self.p2 = Vector(x2, y2)
		self.dist = self.p2 - self.p1
	
	def __str__(self):
		return f"{self.p1} -> {self.p2}"
	
	def is_diagonal(self):
		return (self.dist.x != 0) and (self.dist.y != 0)
	
	def point_set(self):
		dx = 0 if self.dist.x == 0 else -1 if self.dist.x < 0 else 1
		dy = 0 if self.dist.y == 0 else -1 if self.dist.y < 0 else 1
		length = abs(self.dist.x) or abs(self.dist.y)
		points = []
		p = self.p1
		for _ in range(length+1):
			points.append(p)
			p += Vector(dx, dy)
		return points

regex = re.compile('(\d+),(\d+) -> (\d+),(\d+)')
lines = []
for line_def in input_lines:
	m = regex.match(line_def)
	lines.append(Line(*m.groups()))
max_x = max(max(line.p1.x, line.p2.x) for line in lines)
max_y = max(max(line.p1.y, line.p2.y) for line in lines)

# Part 1: Find the number of points where at least two of the horizontal and vertical lines intersect.
hv_lines = [line for line in lines if not line.is_diagonal()]

grid = [[0 for y in range(max_y+1)] for x in range(max_x+1)]
for line in hv_lines:
	points = line.point_set()
	for point in points:
		grid[point.x][point.y] += 1

intersection_points = sum(1 if p > 1 else 0 for col in grid for p in col)
print(f"Part 1: There were {intersection_points} points where at least two lines overlapped")

# Part 2: Now include the diagonal lines! I was expecting a little more from this one, honestly.
# That's what I get for overengineering the answer to part 1.
grid = [[0 for y in range(max_y+1)] for x in range(max_x+1)]
for line in lines:
	points = line.point_set()
	for point in points:
		grid[point.x][point.y] += 1

intersection_points = sum(1 if p > 1 else 0 for col in grid for p in col)
print(f"Part 2: There were {intersection_points} points where at least two lines overlapped")
