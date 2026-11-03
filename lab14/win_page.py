import ctypes
from ctypes import wintypes
import sys

kernel32 = ctypes.windll.kernel32

MEM_RESERVE = 0x00002000
MEM_COMMIT = 0x00001000
MEM_RELEASE = 0x00008000
PAGE_NOACCESS = 0x01
PAGE_READONLY = 0x02
PAGE_READWRITE = 0x04

def main():
	print("--- Старт лабораторной работы ---")

	class SYSTEM_INFO(ctypes.Structure):
		_fields_ = [
			("wProcessorArchitecture", ctypes.c_ushort),
            ("wReserved", ctypes.c_ushort),
            ("dwPageSize", ctypes.c_uint),
            ("lpMinimumApplicationAddress", ctypes.c_void_p),
            ("lpMaximumApplicationAddress", ctypes.c_void_p),
            ("dwActiveProcessorMask", ctypes.c_void_p),
            ("dwNumberOfProcessors", ctypes.c_uint),
            ("dwProcessorType", ctypes.c_uint),
            ("dwAllocationGranularity", ctypes.c_uint),
            ("wProcessorLevel", ctypes.c_ushort),
            ("wProcessorRevision", ctypes.c_ushort)
		]

	si = SYSTEM_INFO()
	kernel32.GetSystemInfo(ctypes.byref(si))
	page_size = si.dwPageSize
	print(f"Размер страницы в вашей системе: {page_size} байт.")

	print("\nШаг 1: Резервирование адресного пространства...")

	# ctypes из C-функции по умолчанию возвращает int, из-за чего ломается программа
	# Поэтому приходится определять возвращаемый тип и типы аргументов вручную
	kernel32.VirtualAlloc.restype = ctypes.c_void_p
	kernel32.VirtualAlloc.argtypes = [
		ctypes.c_void_p,
		ctypes.c_size_t,
		wintypes.DWORD,
		wintypes.DWORD
	]

	kernel32.VirtualProtect.restype = ctypes.c_bool
	kernel32.VirtualProtect.argtypes = [
		ctypes.c_void_p,
		ctypes.c_size_t,
		wintypes.DWORD,
		wintypes.PDWORD
	]

	kernel32.VirtualFree.restype = ctypes.c_bool
	kernel32.VirtualFree.argtypes = [
		ctypes.c_void_p,
		ctypes.c_size_t,
		wintypes.DWORD,
	]
	
	p_memory = kernel32.VirtualAlloc(
		None,
		page_size * 2,
		MEM_RESERVE,
		PAGE_NOACCESS
	)

	if not p_memory:
		print("Не удалось зарезервировать память.")
		sys.exit(1)

	print(f"Адрес зарезервированного региона: {hex(p_memory & (2**64-1))}")

	#print("\nПопытка записи в зарезервированную память...")
	#ctypes.memset(p_memory, 0x41, 1)

	print("\nШаг 2: Выделение физической памяти (COMMIT) с правами READONLY...")
	p_commit = kernel32.VirtualAlloc(
		p_memory,
		page_size,
		MEM_COMMIT,
		PAGE_READONLY
	)

	if not p_commit:
		print("Не удалось выделить физическую память.")
		print(ctypes.windll.kernel32.GetLastError())
		kernel32.VirtualFree(p_memory, 0, MEM_RELEASE)
		sys.exit(1)

	print("Физическая память привязана к адресу. Пробуем прочесть первый байт:")
	first_byte = ctypes.c_char.from_address(p_commit).value
	print(f"Значение байта в памяти (по умолчанию заполнено нулями): {first_byte}")

	print("\nПопытка записи в память с правами READONLY...")
	ctypes.memset(p_commit, 0x42, 1)

	print("\nШаг 3: Изменение прав доступа на READWRITE...")
	old_protect = ctypes.c_ulong()
	success = kernel32.VirtualProtect(
		p_commit, 
		page_size, 
		PAGE_READWRITE, 
		ctypes.byref(old_protect)
	)

	if not success:
		print("Не удалось изменить атрибуты защиты.")
		kernel32.VirtualFree(p_memory, 0, MEM_RELEASE)
		sys.exit(1)

	print("Права успешно изменены. Записываем символ 'X' в память...")
	ctypes.memset(p_commit, ord('X'), 1)

	new_byte = ctypes.c_char.from_address(p_commit).value
	print(f"Прочитанное значение из памяти: {new_byte.decode('utf-8')}")


	print("\nШаг 4: Освобождение памяти...")
	kernel32.VirtualFree(p_memory, 0, MEM_RELEASE)
	print("Память успешно возвращена операционной системе.")

if __name__ == "__main__":
	main()