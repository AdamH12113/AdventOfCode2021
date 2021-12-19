# Process the input. It's just one short line of text so I'm not even going to bother parsing it.
input_target = {'xmin': 117, 'xmax': 164, 'ymin': -140, 'ymax': -89}
example_target = {'xmin': 20, 'xmax': 30, 'ymin': -10, 'ymax': -5}

# Part 1: What is the highest y position that can be reached while still entering the target area?
class Probe:
	def __init__(self, vx, vy):
		self.x = 0
		self.y = 0
		self.vx = vx
		self.vy = vy
		self.highest_y = 0

	def step(self):
		self.x += self.vx
		self.y += self.vy
		self.highest_y = max(self.highest_y, self.y)
		if self.vx > 0:
			self.vx -= 1
		elif self.vx < 0:
			self.vx += 1
		self.vy -= 1

def in_target(target, x, y):
	return x >= target['xmin'] and x <= target['xmax'] and y >= target['ymin'] and y <= target['ymax']

def test_launch(target, vx, vy):
	probe = Probe(vx, vy)
	while probe.x <= target['xmax'] and probe.y >= target['ymin']:
		probe.step()
		if in_target(target, probe.x, probe.y):
			return True, probe.highest_y
	return False, probe.highest_y

def find_highest_y(target):
	highest_y = 0
	for vx in range(1, target['xmax']):
		for vy in range(0, 200):
			success, test_highest_y = test_launch(target, vx, vy)
			if success and test_highest_y > highest_y:
				highest_y = test_highest_y
	return highest_y

hy = find_highest_y(input_target)
print(f"Part 1: The highest y position reached was {hy}")

# Part 2: How many initial velocities cause the probe to hit the target?
def count_successful_velocities(target):
	successes = 0
	for vx in range(1, target['xmax']+1):
		for vy in range(target['ymin'], 200):
			success, _ = test_launch(target, vx, vy)
			if success:
				successes += 1
	return successes

nv = count_successful_velocities(input_target)
print(f"Part 2: The number of successful initial velocities is {nv}")