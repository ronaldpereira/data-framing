from struct import *
import socket

class FrameReader:

	def compareSync(data, SYNC):
		i = 0
		dataPosition = 0

		for character in data:
			dataPosition += 1

			if character == SYNC[i]:
				i += 1

			else:
				i = 0

			if i == 16:
				break

		return (i == 16 if True else False, dataPosition)

	def getLength(data):
		return int(len(data)/8)
		

class Checksum:

	def checksumCalculator(msg):
		s = 0

		for i in range(0, len(msg), 2):
			w = (msg[i]) + ((msg[i+1]) << 8)
			s = Checksum.carryAroundAdd(s, w)

		return (~s & 0xffff)

	def carryAroundAdd(a, b):
		c = a + b

		return (c &0xffff) + (c >> 16)
		
		
SYNC = b'11011100110000000010001111000010' # SYNC constant
rservd = b'0000' # Reserved field - Not used in this project
checksum = b'0000000000000000' # Checksum initialization

input = open('../test/input.txt', 'rb')
output = open('../test/output.txt', 'wb')

data = input.read()

print(data)

length = FrameReader.getLength(data)

msg = SYNC + checksum + b'0000000000000100' + rservd + data

print(msg)

cacatená = pack('>l', length) + pack('>l', length)

print(cacatená)

checksum = Checksum.checksumCalculator(msg)

print(checksum)