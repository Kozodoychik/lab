import mmap
import os

FILE_NAME = "big_data.bin"

def get_rss_memory_kb():
	with open("/proc/self/status", "r") as status_file:
		for line in status_file:
			if line.startswith("VmRSS:"):
				return int(line.split()[1])
	return 0

with open(FILE_NAME, "rb") as f:
	mm = mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ | mmap.PROT_WRITE)

	print(f"[ШАГ 1] Файл 50 МБ спроецирован (MAP_PRIVATE).")
	print(f"Физическая память процесса (VmRSS) до обращения: {get_rss_memory_kb()} КБ")

	for offset in range(0, 20 * 1024 * 1024, 4096):
		_ = mm[offset]

	print(f"\n[ШАГ 2] Прочитано 20 МБ данных из проекции.")
	print(f"Физическая память процесса (VmRSS) после чтения: {get_rss_memory_kb()} КБ")

	for offset in range(0, 20 * 1024 * 1024, 4096):
		mm[offset] = 0xFF
        
	print(f"\n[ШАГ 3] Выполнена запись в 20 МБ проекции (сработал Copy-on-Write).")
	print(f"Физическая память процесса (VmRSS) после записи: {get_rss_memory_kb()} КБ")

	mm.close()


with open(FILE_NAME, "rb") as f:
	first_byte = f.read(1)
	print(f"\n[ПРОВЕРКА ДИСКА] Первый байт файла на диске: {hex(first_byte[0])} (Ожидается 0x0)")