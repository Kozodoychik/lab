import ctypes
import sys

DWORD = ctypes.c_ulong
LPCWSTR = ctypes.c_wchar_p
HANDLE = ctypes.c_void_p

print("--- ШАГ 1: Загрузка управляющей библиотеки kernel32.dll ---")
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

print("\n--- ШАГ 2: Ручное проецирование внешней библиотеки user32.dll в ОЗУ ---")
dll_name = "user32.dll"

# Без этого куска код не работает!!!!!
kernel32.LoadLibraryW.argtypes = [LPCWSTR]
kernel32.LoadLibraryW.restype = HANDLE

# Без этого куска код выдаёт ошибку!!!!!
kernel32.FreeLibrary.argtypes = [HANDLE]
kernel32.FreeLibrary.restype = ctypes.c_int

h_module = kernel32.LoadLibraryW(dll_name)

if not h_module:
	print(f"[ОШИБКА] Не удалось загрузить библиотеку. Код ошибки Windows: {ctypes.get_last_error()}")
	sys.exit(1)

print(f"[УСПЕХ] Библиотека {dll_name} успешно спроецирована в память Ring 3!")
print(f"[НИЗКИЙ УРОВЕНЬ] Дескриптор HMODULE (базовый адрес в ОЗУ): {hex(h_module)}")

print("\n--- ШАГ 3: Парсинг Таблицы Экспорта и поиск адреса функции ---")

kernel32.GetProcAddress.argtypes = [HANDLE, ctypes.c_char_p]
kernel32.GetProcAddress.restype = HANDLE

func_name = b"MessageBoxW"
func_address = kernel32.GetProcAddress(h_module, func_name)

if not func_address:
	print(f"[ОШИБКА] Функция {func_name.decode()} не найдена в Таблице Экспорта DLL!")
	kernel32.FreeLibrary(h_module)
	sys.exit(1)

print(f"[УСПЕХ] Функция найдена!")
print(f"[НИЗКИЙ УРОВЕНЬ] Точный виртуальный адрес кода {func_name.decode()} в ОЗУ: {hex(func_address)}")

print("\n--- ШАГ 4: Динамический вызов функции по найденному адресу ---")

WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_int, HANDLE, LPCWSTR, LPCWSTR, ctypes.c_uint)
message_box_func = WNDPROC(func_address)

print("[ПРОЦЕССОР] Выполняем переход по адресу функции (CALL)...")
message_box_func(0, "Сообщение вызвано через прямой адрес из Таблицы Экспорта!", "Системное программирование", 0)

print("\n--- ШАГ 5: Освобождение системных ресурсов ---")

kernel32.FreeLibrary(h_module)
print("[УСПЕХ] Модуль выгружен из памяти процесса.")