import ctypes
from ctypes import wintypes

class MEM_BASIC_INFO(ctypes.Structure):
	_fields_ = [
		("BaseAddress", ctypes.c_void_p),
		("AllocationBase", ctypes.c_void_p),
		("AllocationProtect", wintypes.DWORD),
		("PartitionId", wintypes.WORD),
		("RegionSize", ctypes.c_size_t),
		("State", wintypes.DWORD),
		("Protect", wintypes.DWORD),
		("Type", wintypes.DWORD),
	]

PROTECT_FLAGS = {
	0x01 : "PAGE_NOACCESS",
	0x02 : "PAGE_READONLY",
	0x04 : "PAGE_READWRITE",
	0x20 : "PAGE_EXECUTE_READ"
}

def analyze_addr(addr):
	mbi = MEM_BASIC_INFO()
	result = ctypes.windll.kernel32.VirtualQuery(
		ctypes.c_void_p(addr),
		ctypes.byref(mbi),
		ctypes.sizeof(mbi)
	)

	if result == 0:
		print("Ошибка вызова VirtualQuery")
		return

	print(f"\n--- Анализ виртуального адреса {hex(addr)} ---")
	print(f"Базовый адрес региона: {hex(mbi.BaseAddress if mbi.BaseAddress else 0)}")
	print(f"Размер региона страниц: {mbi.RegionSize} байт (примерно {mbi.RegionSize // 4096} страниц по 4КБ)")

	current_protect = mbi.Protect
	protect_str = PROTECT_FLAGS.get(current_protect, f"Другой флаг ({hex(current_protect)})")
	print(f"Текущая защита страницы (Protect): {protect_str}")

print("Тест 1: Исследование памяти, где хранится строка Python")
sample_str = "Тестовая строка для лабораторной работы"

str_addr = id(sample_str)
analyze_addr(str_addr)

print("\nТест 2: Исследование нулевого адреса (NULL / nullptr)")
analyze_addr(0)