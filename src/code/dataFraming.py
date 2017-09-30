import struct
import socket
import sys
import threading
SYNC = b'\xdc\xc0\x23\xc2\xdc\xc0\x23\xc2' # SYNC constant

class Communication:

	def receiver(outputPath, host, port, sock):
		while True:
			#recebe o operador do cliente
			frame = sock.recv((2 ** 16) - 1 + 14) # (2 ^ 16) - 1 bytes for payload maximum and + 14 bytes for the header

			frame = Error.verification(frame) # Verifies if the received frame has any errors

			if frame: # If frame is not null, then write it in the output
				with open(outputPath, 'ab') as output:
					output.write(frame[14:])

				output.close()


	def transmitter(inputPath, checksum, rservd, sock):
		with open(inputPath, 'rb') as input:
			data = input.read()

		frameNumber = 0
		FRAMESIZE = (2 ** 16) - 1 # (2 ^ 16) - 1 bytes for payload maximum
		totalLength = Frame.getTotalLength(data)

		while (totalLength - (frameNumber * FRAMESIZE)) > 0:
			checksum = b'\x00\x00'

			dataChunk = Frame.getNextFrameChunk(data, frameNumber, FRAMESIZE)

			frameNumber += 1

			length = Frame.getPayloadLength(dataChunk)

			frame = SYNC + checksum + length + rservd + dataChunk

			checksum = Checksum.checksumCalculator(frame)

			frame = SYNC + checksum + length + rservd + dataChunk

			sock.send(frame)


class Frame:

	def getNextFrameChunk(data, frameNumber, FRAMESIZE):
		startIndex = (frameNumber * FRAMESIZE)
		finishIndex = (frameNumber + 1) * FRAMESIZE

		return data[startIndex : finishIndex]

	def getPayloadLength(dataChunk):
		return struct.pack('>H',(len(dataChunk)))

	def getTotalLength(data):
		return len(data)


class Error:

	def verification(frame):
		while not (Error.syncIsCorrect(frame) and Error.lengthIsCorrect(frame) and Error.checksumIsCorrect(frame)):
			if not frame: # If frame is null
				break

			frame = Error.getNextSync(frame)

		return frame

	def syncIsCorrect(frame):
		return True if frame[0:8] == SYNC else False

	def lengthIsCorrect(frame):
		return True if len(frame[14:]) == int.from_bytes(frame[10:12], byteorder='big') else False

	def checksumIsCorrect(frame):
		frameWithoutChecksum = frame[0:8] + b'\x00\x00' + frame[10:]
		return True if Checksum.checksumCalculator(frameWithoutChecksum) == frame[8:10] else False

	def getNextSync(frame):
		frame = frame[1:] # Discard the first byte
		while frame[0:8] != SYNC: # Tries to match the first 8 bytes with the SYNC
			if not frame: # If the actual frame is null
				break

			frame = frame[1:] # If the SYNC is wrong, exclude the first byte from frame and try again

		return frame

class Checksum:

	def checksumCalculator(msg):
		s = 0

		if len(msg) % 2 != 0:
			msg += b'\x00'

		for i in range(0, len(msg), 2):
			w = (msg[i] + (msg[i+1]) << 16)
			s = Checksum.carryAroundAdd(s, w)

		return struct.pack('>H', ~s & 0xffff)

	def carryAroundAdd(a, b):
		c = a + b

		return (c & 0xffff) + (c >> 16)



checksum = b'\x00\x00' # Checksum initialization
rservd = b'\x00\x00' # Reserved field - Not used in this project

host = sys.argv[3]
port = int(sys.argv[4])
mode = sys.argv[5]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if mode == 'passivo':
	sock.bind((host, port))
	sock.listen(5)
	(clientSocket, address) = sock.accept()
	threading._start_new_thread(Communication.receiver, (sys.argv[2], host, port, clientSocket))
	threading._start_new_thread(Communication.transmitter, (sys.argv[1], checksum, rservd, clientSocket))

elif mode == 'ativo':
	sock.connect((host, port))
	threading._start_new_thread(Communication.transmitter, (sys.argv[1], checksum, rservd, sock))
	threading._start_new_thread(Communication.receiver, (sys.argv[2], host, port, sock))

while 1:
	pass