import random

FILE_NAME = "big_data.bin"
FILE_SIZE = 50 * 1024 * 1024

with open(FILE_NAME, "rb") as f:
	for _ in range(10000):
		offset = random.randint(0, FILE_SIZE - 10)
		f.seek(offset)
		data = f.read(4)
