import struct
import socket
import sys

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
		return struct.pack('>H',(len(data)))


class Checksum:

	def checksumCalculator(msg):
		s = 0

		for i in range(0, len(msg), 2):
			w = (msg[i] + (msg[i+1]) << 16)
			s = Checksum.carryAroundAdd(s, w)

		return struct.pack('>H', ~s & 0xffff)

	def carryAroundAdd(a, b):
		c = a + b

		return (c & 0xffff) + (c >> 16)


SYNC = b'\xdc\xc0\x23\xc2\xdc\xc0\x23\xc2' # SYNC constant
rservd = b'\x00\x00' # Reserved field - Not used in this project
checksum = b'\x00\x00' # Checksum initialization

with open(sys.argv[1], 'rb') as input:
	data = input.read()

length = FrameReader.getLength(data)

frame = SYNC + checksum + length + rservd + data

print(frame)

checksum = Checksum.checksumCalculator(frame)

print(checksum)

frame = SYNC + checksum + length + rservd + data

print(frame)

with open(sys.argv[2], 'wb') as output:
	output.write(frame)