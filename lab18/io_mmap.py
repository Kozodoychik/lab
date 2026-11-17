import mmap
import random

FILE_NAME = "big_data.bin"
FILE_SIZE = 50 * 1024 * 1024

with open(FILE_NAME, "rb") as f:
	with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
		for _ in range(10000):
			offset = random.randint(0, FILE_SIZE - 10)
			data = mm[offset : offset + 4]
