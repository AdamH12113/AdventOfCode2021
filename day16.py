# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input16.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. It's a single large hexadecimal string that describes nested packet data.
input_str = input_lines[0]
examples = ["D2FE28", "38006F45291200", "EE00D40C823060", "8A004A801A8002F478", "620080001611562C8802118E34", "C0015000016115A2E0802F182340", "A0016C880162017C3686B18A3D4780"]
input_str = examples[1]

# Part 1: What is the sum of the version numbers in all of the packets?
class Packet:
	def __init__(self, pver, ptype):
		self.pver = pver
		self.ptype = ptype
		self.contents = None

class BitBuffer:
	def __init__(self, bit_string):
		self.bits = [b for b in bit_string]

	def pop(self, n):
		popped_num = int(''.join(self.bits[:n]), 2)
		self.bits = self.bits[n:]
		return popped_num
	
	def __getitem__(self, key):
		return BitBuffer(self.bits[key])
	
	def __len__(self):
		return len(self.bits)

def hex_to_bin(hex_string):
	bits = []
	for h in hex_string:
		bits.extend(b for b in format(int(h, 16), '04b'))
	return ''.join(bits)


def parse_packets(bp):
	while len(bp) >= 3:
		pver = bp.pop(3)
		if pver == 0:
			break
		ptype = bp.pop(3)
		print(pver, ptype, end=' ')
		
		if ptype == 4:
			val = 0
			stop = False
			while not stop:
				field = bp.pop(5)
				val = (val << 4) + (field & 0x0f)
				stop = bool(field & 0x10 == 0x00)
			print(f"literal {val}")
		else:
			length_type = bp.pop(1)
			if length_type == 0:
				sub_packets_len = bp.pop(15)
				print(f"operator blen {sub_packets_len}")
				parse_packets(bp[:sub_packets_len])
				bp.pop(sub_packets_len)

bits = BitBuffer(hex_to_bin(input_str))
parse_packets(bits)
