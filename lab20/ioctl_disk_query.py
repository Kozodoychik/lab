import ctypes
from ctypes import wintypes
import sys

# --- КОНСТАНТЫ WINDOWS API ---
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x00000080
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

# 32-битный управляющий код IOCTL_DISK_GET_DRIVE_GEOMETRY
IOCTL_DISK_GET_DRIVE_GEOMETRY = 0x00070000

# Словарь расшифровки аппаратного типа носителя (enum MEDIA_TYPE)
MEDIA_TYPES = {
	0: "Unknown (Неизвестный тип)",
	11: "RemovableMedia (Съемный носитель / Флешка)",
	12: "FixedMedia (Фиксированный жесткий диск / SSD)"
}

# --- СТРУКТУРА ЯДРА DISK_GEOMETRY (24 байта) ---
# В эту структуру драйвер disk.sys запишет аппаратные параметры накопителя
class DISK_GEOMETRY(ctypes.Structure):
	_fields_ = [
		("Cylinders", ctypes.c_int64),		  # 8 байт: количество цилиндров
		("MediaType", ctypes.c_int),			# 4 байта: тип носителя
		("TracksPerCylinder", wintypes.DWORD),  # 4 байта: дорожек на цилиндр
		("SectorsPerTrack", wintypes.DWORD),	# 4 байта: секторов на дорожку
		("BytesPerSector", wintypes.DWORD),	 # 4 байта: физический размер сектора в байтах
	]

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Настраиваем типы аргументов для 64-битного вызова CreateFileW
kernel32.CreateFileW.argtypes = [
	wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
	ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE
]
kernel32.CreateFileW.restype = wintypes.HANDLE

# Настраиваем типы аргументов для DeviceIoControl
kernel32.DeviceIoControl.argtypes = [
	wintypes.HANDLE, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD,
	ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p
]
kernel32.DeviceIoControl.restype = wintypes.BOOL

device_path = r"\\.\PhysicalDrive0"
print(f"[RING 3] Попытка открыть символическую ссылку устройства: {device_path}")

# ШАГ 1: Открываем дескриптор драйвера.
# Обратите внимание: второй аргумент (dwDesiredAccess) равен 0 (запрос только метаданных).
h_device = kernel32.CreateFileW(
	device_path,
	0,					  # Права доступа: 0 (без чтения/записи секторов)
	0x00000001 | 0x00000002,# FILE_SHARE_READ | FILE_SHARE_WRITE
	None,
	OPEN_EXISTING,
	FILE_ATTRIBUTE_NORMAL,
	None
)

if h_device == INVALID_HANDLE_VALUE:
	print(f"[ОШИБКА ЯДРА] Не удалось открыть устройство. Код ошибки Win32: {ctypes.get_last_error()}")
	sys.exit(1)

print(f"[УСПЕХ] Дескриптор драйвера получен! HANDLE = {hex(h_device)}")

# Выделяем буфер в памяти Ring 3 под ответ драйвера
geometry = DISK_GEOMETRY()
bytes_returned = wintypes.DWORD(0)

print(f"[I/O MANAGER] Отправляем пакет IRP с кодом IOCTL {hex(IOCTL_DISK_GET_DRIVE_GEOMETRY)}...")

# ШАГ 2: Вызываем DeviceIoControl (переход в Ring 0)
success = kernel32.DeviceIoControl(
	h_device,
	IOCTL_DISK_GET_DRIVE_GEOMETRY,
	None, 0,							# Входной буфер не требуется
	ctypes.byref(geometry),				# Указатель на выходной буфер в памяти процесса
	ctypes.sizeof(geometry),			# Размер выходного буфера (24 байта)
	ctypes.byref(bytes_returned),		# Сюда ядро запишет, сколько байт реально вернул драйвер
	None
)

if not success:
	print(f"[ОШИБКА ДРАЙВЕРА] Сбой DeviceIoControl. Код ошибки Win32: {ctypes.get_last_error()}")
	kernel32.CloseHandle(h_device)
	sys.exit(1)

print(f"[УСПЕХ] Драйвер вернул {bytes_returned.value} байт аппаратной конфигурации:\n")
print(f"  Тип носителя (MediaType):		{MEDIA_TYPES.get(geometry.MediaType, geometry.MediaType)}")
print(f"  Количество цилиндров:			{geometry.Cylinders}")
print(f"  Дорожек на цилиндр:			{geometry.TracksPerCylinder}")
print(f"  Секторов на дорожку:			{geometry.SectorsPerTrack}")
print(f"  Размер физического сектора:		{geometry.BytesPerSector} байт")

# Вычисляем общий объем физического устройства по формуле геометрии
total_bytes = (geometry.Cylinders * geometry.TracksPerCylinder * geometry.SectorsPerTrack * geometry.BytesPerSector)
print(f"  Расчетный объем устройства:		{total_bytes / (1024**3):.2f} ГБ")

raw_sector = ctypes.create_string_buffer(512)
read_bytes = wintypes.DWORD(0)
res = kernel32.ReadFile(h_device, raw_sector, 512, ctypes.byref(read_bytes), None)
print(f"Результат ReadFile: {res}, Код ошибки: {ctypes.get_last_error()}")

# ШАГ 3: Закрываем дескриптор (генерирует пакет IRP_MJ_CLOSE)
kernel32.CloseHandle(h_device)
print("\n[СИСТЕМА] Дескриптор устройства закрыт.")