import ctypes
from ctypes import wintypes
import time
import struct

# --- КОНСТАНТЫ WINDOWS API ---
INVALID_HANDLE_VALUE	= ctypes.c_void_p(-1).value
PAGE_READWRITE			= 0x04
FILE_MAP_ALL_ACCESS		= 0x000F001F
MEM_SIZE				= 4096  # Выделяем ровно 1 стандартную страницу памяти (4 КБ)
MAPPING_NAME			= "Local\SysProgCoolerTelemetry"

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Настраиваем точные типы аргументов для 64-битной архитектуры Windows
kernel32.CreateFileMappingW.argtypes = [
	wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, 
	wintypes.DWORD, wintypes.DWORD, wintypes.LPCWSTR
]
kernel32.CreateFileMappingW.restype = wintypes.HANDLE

kernel32.MapViewOfFile.argtypes = [
	wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, 
	wintypes.DWORD, ctypes.c_size_t
]
kernel32.MapViewOfFile.restype = ctypes.c_void_p

print("[ПОСТАВЩИК] Запрашиваем у ядра анонимный объект проекции памяти...")
# 1. Создаем объект проекции без файла на диске (INVALID_HANDLE_VALUE)
h_map_file = kernel32.CreateFileMappingW(
	INVALID_HANDLE_VALUE, None, PAGE_READWRITE, 0, MEM_SIZE, MAPPING_NAME
)

if not h_map_file:
	print(f"[ОШИБКА] Сбой CreateFileMappingW. Код: {ctypes.get_last_error()}")
	exit(1)

# 2. Отображаем страницу ядра в виртуальную память нашего процесса (создаем View)
p_buf = kernel32.MapViewOfFile(h_map_file, FILE_MAP_ALL_ACCESS, 0, 0, MEM_SIZE)

if not p_buf:
	print(f"[ОШИБКА] Сбой MapViewOfFile. Код: {ctypes.get_last_error()}")
	kernel32.CloseHandle(h_map_file)
	exit(1)

print(f"[УСПЕХ] Страница ОЗУ спроецирована в виртуальное пространство процесса!")
print(f"[НИЗКИЙ УРОВЕНЬ] Базовый виртуальный адрес буфера в этом процессе: {hex(p_buf)}")
print("[ПОСТАВЩИК] Начинаем прямую запись байт в ОЗУ. Запустите второй скрипт (shm_reader.py)!\n")

try:
	counter = 1
	while True:
		# Упаковываем два числа (ID пакета и условные обороты кулера) в 8 сырых байт (два 32-битных int)
		rpm_value = 1200 + (counter % 300)
		raw_bytes = struct.pack("ii", counter, rpm_value)
		
		# Прямое копирование байт в виртуальную память (аналог инструкции REP MOVSB на ассемблере)
		ctypes.memmove(p_buf, raw_bytes, len(raw_bytes))
		
		print(f"[ЗАПИСЬ В ОЗУ] Пакет #{counter} | Значение: {rpm_value} -> записано по адресу {hex(p_buf)}")
		counter += 1
		time.sleep(1)

except KeyboardInterrupt:
	print("\n[ПОСТАВЩИК] Остановка работы пользователем.")
finally:
	# Обязательное освобождение ресурсов ядра
	kernel32.UnmapViewOfFile(ctypes.c_void_p(p_buf))
	kernel32.CloseHandle(h_map_file)
	print("[СИСТЕМА] Проекция закрыта, дескриптор ядра освобожден.")