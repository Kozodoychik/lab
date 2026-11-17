import ctypes
from ctypes import wintypes
import time
import struct

FILE_MAP_READ = 0x0004
MEM_SIZE = 4096
MAPPING_NAME = "Local\SysProgCoolerTelemetry"

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

kernel32.OpenFileMappingW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
kernel32.OpenFileMappingW.restype = wintypes.HANDLE

kernel32.MapViewOfFile.argtypes = [
wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD,
wintypes.DWORD, ctypes.c_size_t
]
kernel32.MapViewOfFile.restype = ctypes.c_void_p

print("[ПОТРЕБИТЕЛЬ] Поиск существующей проекции памяти в таблицах ядра Windows...")

# 1. Подключаемся к уже созданному объекту проекции по его имени
h_map_file = kernel32.OpenFileMappingW(FILE_MAP_READ, False, MAPPING_NAME)

if not h_map_file:
	print("[ОШИБКА] Объект памяти не найден! Сначала запустите shm_writer.py.")
	exit(1)

# 2. Проецируем эту же физическую страницу в НАШЕ виртуальное адресное пространство
p_buf = kernel32.MapViewOfFile(h_map_file, FILE_MAP_READ, 0, 0, MEM_SIZE)

if not p_buf:
	print(f"[ОШИБКА] Сбой MapViewOfFile. Код: {ctypes.get_last_error()}")
	kernel32.CloseHandle(h_map_file)
	exit(1)

print(f"[УСПЕХ] Подключение выполнено!")
print(f"[НИЗКИЙ УРОВЕНЬ] Базовый виртуальный адрес буфера В ЭТОМ ПРОЦЕССЕ: {hex(p_buf)}\n")

try:
	while True:
		# Считываем 8 сырых байт напрямую из виртуальной памяти процесса
		raw_bytes = ctypes.string_at(p_buf, 8)
		packet_id, rpm_value = struct.unpack("ii", raw_bytes)
		
		print(f"[ЧТЕНИЕ ИЗ ОЗУ] Считано по адресу {hex(p_buf)} -> Пакет #{packet_id} | Значение: {rpm_value}")
		time.sleep(1)

except KeyboardInterrupt:
	print("\n[ПОТРЕБИТЕЛЬ] Завершение работы.")
finally:
	kernel32.UnmapViewOfFile(ctypes.c_void_p(p_buf))
	kernel32.CloseHandle(h_map_file)