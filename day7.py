# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input7.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]
example_input = ["16,1,2,0,4,2,7,1,2,14"]
#input_lines = example_input

# Process the input. This time it's just a list of integers representing the horizontal position
# of each crab.
positions = [int(num) for num in input_lines[0].split(',')]

# Part 1: Find a position to converge on that costs the least fuel.
def compute_fuel_consumption(positions, convergence_point):
	sum = 0
	for pos in positions:
		sum += abs(convergence_point - pos)
	return sum

def find_min_fuel_consumption(positions, fuel_func):
	min_fuel_convergence_point = 0
	min_fuel_consumption = (1 << 48)
	for convergence_point in range(min(positions), max(positions)+1):
		fuel_consumption = fuel_func(positions, convergence_point)
		if fuel_consumption < min_fuel_consumption:
			min_fuel_consumption = fuel_consumption
			min_fuel_convergence_point = convergence_point
	return min_fuel_convergence_point, min_fuel_consumption

convergence_point, fuel_consumption = find_min_fuel_consumption(positions, compute_fuel_consumption)
print(f"Part 1: The best position is {convergence_point} with total fuel usage of {fuel_consumption}")

# Part 2: Same as the above, but now movement costs an additional unit of fuel for each new step.
# The formula for this is n(n+1)/2.
def compute_fuel_consumption2(positions, convergence_point):
	sum = 0
	for pos in positions:
		dist = abs(convergence_point - pos)
		sum += dist*(dist+1)/2
	return sum

convergence_point, fuel_consumption = find_min_fuel_consumption(positions, compute_fuel_consumption2)
print(f"Part 2: The best position is {convergence_point} with total fuel usage of {fuel_consumption}")
