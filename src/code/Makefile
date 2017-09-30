PORT = 55545

passivo:
	python3 dataFraming.py ../test/input.txt ../test/outputpassivo.bin 127.0.0.1 $(PORT) passivo

ativo:
	python3 dataFraming.py ../test/input.bin ../test/outputativo.txt 127.0.0.1 $(PORT) ativo

passivopdf:
	python3 dataFraming.py ../test/quickStart.pdf ../test/outputspec.pdf 127.0.0.1 $(PORT) passivo

ativopdf:
	python3 dataFraming.py ../../reference/spec-tp1.pdf ../test/outputquickStart.pdf 127.0.0.1 $(PORT) ativo