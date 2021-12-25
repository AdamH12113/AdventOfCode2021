# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('example19.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. 

x <- 1
z <- 25 + input + 6








x <- (z mod 26) - 9
x <- x != input

z <- z // 26      # Or 1   # 0 if z < 26
z <- z + x*25
z <- z + x*(input + 6)









