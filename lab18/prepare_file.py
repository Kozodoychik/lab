import os

FILE_NAME = "big_data.bin"
FILE_SIZE = 50 * 1024 * 1024

print(f"[СИСТЕМА] Создание бинарного файла {FILE_NAME} размером 50 МБ...")
with open(FILE_NAME, "wb") as f:
	f.seek(FILE_SIZE - 5)
	f.write(b"END!!")

print("[УСПЕХ] Файл сформирован на диске.")