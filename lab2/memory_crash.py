import ctypes
from ctypes import wintypes

PAGE_NOACCESS = 0x1

buff = ctypes.c_long(500)
buff_addr = ctypes.addressof(buff)

print(f"Буфер создан по адрему: {hex(buff_addr)}")
print(f"Текущее значение в буфере: {buff.value}")

print("\nОбращаемся к подсистеме памяти: принудительно устанавливаем флаг PAGE_NOACCESS для этой страницы...")
old_protect = wintypes.DWORD()

success = ctypes.windll.kernel32.VirtualProtect(
	ctypes.c_void_p(buff_addr),
	ctypes.sizeof(buff),
	PAGE_NOACCESS,
	ctypes.byref(old_protect)
)

if success:
	print("Флаг защиты успешно изменен на PAGE_NOACCESS!")
	print("Сейчас программа попытается прочитать данные по заблокированному адресу...")

	invalid_read = buff.value
	print(f"Этот текст никогда не напечатается (эх): {invalid_read}")
else:
	print("Не удалось изменить флаги защиты.")