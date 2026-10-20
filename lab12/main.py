import ctypes
import os

lib_path = os.path.abspath("./libmylib.so")

print(f"[ПРОГРАММА] Загружаем внешнюю ассемблерную библиотеку: {lib_path}")

try:
	my_asm_lib = ctypes.CDLL(lib_path)
except OSError as e:
	print(f"[КРИТИЧЕСКАЯ ОШИБКА]: Не удалось загрузить .so. Проверьте пути. Данные: {e}")
	exit(1)

print("[УСПЕХ] Библиотека спроецирована в память процесса.")

secret_data = "System Programming 2026"

bin_buffer = bytearray(secret_data.encode("utf-8"))
buffer_len = len(bin_buffer)

c_buffer = (ctypes.c_char * buffer_len).from_buffer(bin_buffer)
print(f"\nИсходная строка в памяти: '{secret_data}'")
print(f"Сырые байты до обработки: {list(bin_buffer)}")

print("\n[ПРОЦЕССОР] Передаем управление в libmylib.so -> функция asm_encrypt...")

my_asm_lib.asm_encrypt(c_buffer, buffer_len)

print(f"Сырые байты после шифрования (XOR): {list(bin_buffer)}")
print(f"Зашифрованная строка в консоли: '{bin_buffer.decode('utf-8', errors='ignore')}'")

print("\n[ПРОЦЕССОР] Повторный вызов asm_encrypt для расшифровки...")

my_asm_lib.asm_encrypt(c_buffer, buffer_len)

print(f"Байты после повторного XOR: {list(bin_buffer)}")
print(f"Восстановленная строка: '{bin_buffer.decode('utf-8')}'")