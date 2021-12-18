import math, operator

# Read the input file. Ideally we would use a generator here, but then we'd
# have to keep the file handle alive.
with open('input16.txt', 'rt') as f:
	input_lines = [line.rstrip() for line in f]

# Process the input. It's a single large hexadecimal string that describes nested packet data.
input_str = input_lines[0]
examples = ["D2FE28", "38006F45291200", "EE00D40C823060", "8A004A801A8002F478", "620080001611562C8802118E34", "C0015000016115A2E0802F182340", "A0016C880162017C3686B18A3D4780"]

# Part 1: What is the sum of the version numbers in all of the packets?
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
	
	def __str__(self):
		return ''.join(self.bits)

def hex_to_bin(hex_string):
	bits = []
	for h in hex_string:
		bits.extend(b for b in format(int(h, 16), '04b'))
	return ''.join(bits)


def calc_version_sum(bp, npackets=None, indent=0):
	version_sum = 0
	packets_parsed = 0
	while (npackets and packets_parsed < npackets) or (not npackets and len(bp) > 6):
		pver = bp.pop(3)
		ptype = bp.pop(3)
		version_sum += pver
		
		if ptype == 4 and len(bp) >= 5:
			val = 0
			stop = False
			while not stop:
				field = bp.pop(5)
				val = (val << 4) + (field & 0x0f)
				stop = bool(field & 0x10 == 0x00)
		else:
			length_type = bp.pop(1)
			if length_type == 0 and len(bp) > 15:
				sub_packets_len = bp.pop(15)
				version_sum += calc_version_sum(bp[:sub_packets_len], indent=indent+1)
				bp.pop(sub_packets_len)
			elif len(bp) > 11:
				num_sub_packets = bp.pop(11)
				version_sum += calc_version_sum(bp, num_sub_packets, indent+1)
		packets_parsed += 1
	return version_sum

bits = BitBuffer(hex_to_bin(input_str))
version_sum = calc_version_sum(bits)
print(f"Part 1: The sum of the packet version numbers is {version_sum}")

# Part 2: Determine the value of the outermost packet using the operator types.
class LiteralPacket:
	def __init__(self, value):
		self.value = value
	
	def __call__(self):
		return self.value
	
	def __str__(self):
		return f"Lit {self.value}"
	
class OperatorPacket:
	def __init__(self, ptype, subpackets):
		operators = {0: sum, 1: math.prod, 2: min, 3: max, 5: operator.gt, 6: operator.lt, 7: operator.eq}
		self.operator = operators[ptype]
		self.contents = subpackets
	
	# Ugly hack because I'm tired
	def __call__(self):
		operands = [p() for p in self.contents]
		try:
			return int(self.operator(operands))
		except:
			return int(self.operator(*operands))
	
	def __str__(self):
		return f"Op {[str(p) for p in self.contents]}"
	def __repr__(self):
		return f"Op {[str(p) for p in self.contents]}"

examples = ['C200B40A82', '04005AC33890', '880086C3E88112', 'CE00C43D881120', 'D8005AC2A8F0',
            'F600BC2D8F', '9C005AC2F8F0', '9C0141080250320F1802104A08']

def parse_packets(bp, npackets=None):
	packets_parsed = 0
	packets = []
	while (npackets and packets_parsed < npackets) or (not npackets and len(bp) > 6):
		pver = bp.pop(3)
		ptype = bp.pop(3)
		
		if ptype == 4 and len(bp) >= 5:
			val = 0
			stop = False
			while not stop:
				field = bp.pop(5)
				val = (val << 4) + (field & 0x0f)
				stop = bool(field & 0x10 == 0x00)
			packets.append(LiteralPacket(val))
		else:
			length_type = bp.pop(1)
			if length_type == 0 and len(bp) > 15:
				sub_packets_len = bp.pop(15)
				packets.append(OperatorPacket(ptype, parse_packets(bp[:sub_packets_len])))
				bp.pop(sub_packets_len)
			elif len(bp) > 11:
				num_sub_packets = bp.pop(11)
				packets.append(OperatorPacket(ptype, parse_packets(bp, num_sub_packets)))
		packets_parsed += 1
	return packets

bits = BitBuffer(hex_to_bin(input_str))
packets = parse_packets(bits)
print(f"Part 2: The value of the outermost packet is {packets[0]()}")
