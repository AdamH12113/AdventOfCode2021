from colorama import init, Style, Fore
init()

# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input9.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. We get a grid of numbers representing a heightmap.
heightmap = [[int(col) for col in row] for row in input_lines]
rmax = len(heightmap) - 1
cmax = len(heightmap[0]) - 1

# Part 1: Find the low points -- locations that are lower than any of the adjacent locations. Edges
# are treated as higher than any location in the heightmap.
def is_low_point(hmap, r, c):
	h = hmap[r][c]
	lower_than_north = (r == 0) or (h < hmap[r-1][c])
	lower_than_south = (r == rmax) or (h < hmap[r+1][c])
	lower_than_west = (c == 0) or (h < hmap[r][c-1])
	lower_than_east = (c == cmax) or (h < hmap[r][c+1])
	return lower_than_north and lower_than_south and lower_than_west and lower_than_east

low_points = [(r, c) for r in range(0, rmax+1) for c in range(0, cmax+1) if is_low_point(heightmap, r, c)]
risk_level_sum = sum(heightmap[r][c] + 1 for (r,c) in low_points)
print(f"Part 1: The sum of the low points' risk levels is {risk_level_sum}")

# Part 2: Find the sizes of the three largest basins. A basin is all locations that eventually flow
# downward to a low point. Every location except the ones with a height of 9 are in basins.
def inside_box(r, c):
	return (r >= 0 and r <= rmax and c >= 0 and c <= cmax)

# Find all the points in a basin starting at the low point
def get_basin_points(hmap, low_point_r, low_point_c):
	basin_points = {(low_point_r, low_point_c)}
	queue = [(low_point_r, low_point_c)]
	while len(queue) > 0:
		queue_r, queue_c = queue.pop()
		for (dr, dc) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			r = queue_r + dr
			c = queue_c + dc
			if inside_box(r, c) and (r, c) not in basin_points and not hmap[r][c] == 9:
				queue.insert(0, (r, c))
				basin_points.add((r, c))
	return basin_points

basin_sizes = []
for point in low_points:
	r, c = point
	basin_points = get_basin_points(heightmap, r, c)
	basin_sizes.append(len(basin_points))
basin_sizes.sort(reverse=True)
print(f"Part 2: The product of the three largest basin sizes is {basin_sizes[0] * basin_sizes[1] * basin_sizes[2]}")

