import re

# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input22.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. Each line consists of the word "on" or "off" followed by a list of X, Y, and Z
# coordinate ranges.
parsed_input = []
for line in input_lines:
	on_off = line.split(' ')[0]
	ranges = [int(n) for n in re.findall(r'-?\d+', line[2:])]
	parsed_input.append([on_off, *ranges])

# Part 1: Determine how many cubes are on after executing the reboot steps in a 50x50x50 area. I'm
# going to make a halfhearted attempt to handle part 2 by using a sparse representation of on cubes.
on_cubes = set()
for step in parsed_input:
	on_noff = step[0] == 'on'
	x1 = step[1]
	x2 = step[2]
	y1 = step[3]
	y2 = step[4]
	z1 = step[5]
	z2 = step[6]
	if x1 > 50 or x1 < -50:
		continue
	for x in range(min(x1, x2), max(x1, x2)+1):
		for y in range(min(y1, y2), max(y1, y2)+1):
			for z in range(min(z1, z2), max(z1, z2)+1):
				if on_noff:
					on_cubes.add((x, y, z))
				else:
					on_cubes.discard((x, y, z))
print(f"Part 1: The number of cubes that are on is {len(on_cubes)}")

# Part 2: Oh god oh fuck it's another puzzle that's computationally infeasible unless you use the
# one weird trick. Okay, not ONE weird trick, or even one WEIRD trick, but still, I could use an
# easy day for a change. Oh well. I suppose I'll have to treat intersections as breaking one cuboid
# into multiple cuboids.
class Cuboid:
	def __init__(self, state, x1, x2, y1, y2, z1, z2):
		self.state = (state == 'on')
		self.xmin = min(x1, x2)
		self.xmax = max(x1, x2)
		self.ymin = min(y1, y2)
		self.ymax = max(y1, y2)
		self.zmin = min(z1, z2)
		self.zmax = max(z1, z2)
	
	def size(self)
		return (1 + self.xmax - self.xmin) * (1 + self.ymax - self.ymin) * (1 + self.zmax - self.zmin)
	
	def evaluate_x_overlap(self, other):
		if self.xmin > other.xmax or other.xmin > self.xmax:
			return 'disjoint'
		elif self.xmin == other.xmin and self.xmax == other.xmax:
			return 'equal'
		elif self.xmin >= other.xmin and self.xmin <= other.xmax and self.xmax >= other.xmin and self.xmax <= other.xmax:
			return 'inside'
		elif other.xmin >= self.xmin and other.xmin <= other.xmax and other.xmax >= self.xmin and other.xmax <= self.xmax:
			return 'contains'
		else:
			return 'overlaps'

	def evaluate_y_overlap(self, other):
		if self.ymin > other.ymax or other.ymin > self.ymax:
			return 'disjoint'
		elif self.ymin == other.ymin and self.ymax == other.ymax:
			return 'equal'
		elif self.ymin >= other.ymin and self.ymin <= other.ymax and self.ymax >= other.ymin and self.ymax <= other.ymax:
			return 'inside'
		elif other.ymin >= self.ymin and other.ymin <= other.ymax and other.ymax >= self.ymin and other.ymax <= self.ymax:
			return 'contains'
		else:
			return 'overlaps'

	def evaluate_z_overlap(self, other):
		if self.zmin > other.zmax or other.zmin > self.zmax:
			return 'disjoint'
		elif self.zmin == other.zmin and self.zmax == other.zmax:
			return 'equal'
		elif self.zmin >= other.zmin and self.zmin <= other.zmax and self.zmax >= other.zmin and self.zmax <= other.zmax:
			return 'inside'
		elif other.zmin >= self.zmin and other.zmin <= other.zmax and other.zmax >= self.zmin and other.zmax <= self.zmax:
			return 'contains'
		else:
			return 'overlaps'
	
	def evaluate_xyz_overlap(self, other):
		return self.evaluate_x_overlap(other), self.evaluate_y_overlap(other), self.evaluate_z_overlap(other)

	def intersects(self, other):
		return all(oe != 'disjoint' for oe in self.evaluate_xyz_overlap(other))
	
	def contains(self, other):
		return all(oe == 'contains' for oe in self.evaluate_xyz_overlap(other))

	def inside(self, other):
		return all(oe == 'inside' for oe in self.evaluate_xyz_overlap(other))
	
	def overlaps(self, other):
		return self.intersects(other) and not (self.contains(other) or self.inside(other))
	
	def __str__(self):
		return f"{self.state} {self.xmin} {self.xmax} {self.ymin} {self.ymax} {self.zmin} {self.zmax}"
	
	# We don't have any one-dimensional overlaps, so 
	def split_around(self, other):
		pass

cuboids = []
for step in parsed_input:
	cuboids.append(Cuboid(*step))












