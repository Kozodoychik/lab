import ctypes
import time
import os
import random

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class SMALL_RECT(ctypes.Structure):
    _fields_ = [
        ("Left", ctypes.c_short), ("Top", ctypes.c_short),
        ("Right", ctypes.c_short), ("Bottom", ctypes.c_short)
    ]

class CHAR_UNION(ctypes.Union):
    _fields_ = [("UnicodeChar", ctypes.c_wchar), ("AsciiChar", ctypes.c_char)]

class CHAR_INFO(ctypes.Structure):
    _fields_ = [("Char", CHAR_UNION), ("Attributes", ctypes.c_ushort)]

FOREGROUND_BLUE      = 0x0001
FOREGROUND_GREEN     = 0x0002
FOREGROUND_RED       = 0x0004
FOREGROUND_INTENSITY = 0x0008
BACKGROUND_BLUE      = 0x0010
BACKGROUND_GREEN     = 0x0020
BACKGROUND_RED       = 0x0040
BACKGROUND_INTENSITY = 0x0080

COLOR_TEXT_WHITE  = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY
COLOR_TEXT_GREEN  = FOREGROUND_GREEN | FOREGROUND_INTENSITY
COLOR_TEXT_RED    = FOREGROUND_RED | FOREGROUND_INTENSITY
COLOR_BG_NAVY     = BACKGROUND_BLUE | BACKGROUND_INTENSITY

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 25

h_original_out = kernel32.GetStdHandle(-11)

print("[СИСТЕМА] Запрашиваем у ядра создание дополнительного скрытого буфера экрана (бэк-буфера)...")

h_back_buffer = kernel32.CreateConsoleScreenBuffer(
    0x80000000 | 0x40000000,
    0, None, 1, None
)

if h_back_buffer == -1 or h_back_buffer is None:
    print(f"[ОШИБКА] Не удалось создать буфер экрана. Код: {ctypes.get_last_error()}")
    exit(1)

kernel32.SetConsoleActiveScreenBuffer(h_back_buffer)

buffer_size = SCREEN_WIDTH * SCREEN_HEIGHT
local_memory_buffer = (CHAR_INFO * buffer_size)()

def clear_local_buffer(char=' ', attr=0):
	#os.system("cls")
    for i in range(buffer_size):
        local_memory_buffer[i].Char.UnicodeChar = char
        local_memory_buffer[i].Attributes = attr

def write_string(text, x, y, attr):
    #print(text)
    if y < 0 or y >= SCREEN_HEIGHT: return
    start_index = y * SCREEN_WIDTH + x
    for idx, char in enumerate(text):
        if x + idx >= SCREEN_WIDTH: break
        local_memory_buffer[start_index + idx].Char.UnicodeChar = char
        local_memory_buffer[start_index + idx].Attributes = attr

buffer_size_coord = COORD(SCREEN_WIDTH, SCREEN_HEIGHT)
buffer_coord = COORD(0, 0)
write_region = SMALL_RECT(0, 0, SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1)

fan_frames = ['|', '/', '-', '']
frame_idx = 0

print("[ПРОЦЕССОР] Запуск высокопроизводительного цикла отрисовки кадра...")
try:
    for tick in range(100):
        clear_local_buffer(' ', COLOR_BG_NAVY)
        
        write_string("=== НИЗКОУРОВНЕВЫЙ МОНИТОР БУФЕРА ЭКРАНА (WINDOWS API) ===", 12, 2, COLOR_TEXT_WHITE | COLOR_BG_NAVY)
        write_string(f"Текущий кадр рендеринга: {tick:03d} / 100", 5, 5, COLOR_TEXT_GREEN | COLOR_BG_NAVY)
        
        current_data = random.randint(1100, 1600)
        status_color = COLOR_TEXT_GREEN if current_data > 1200 else COLOR_TEXT_RED
        
        write_string(f"Показания системного датчика: {current_data} ед.", 5, 7, COLOR_TEXT_WHITE | COLOR_BG_NAVY)
        
        current_frame = fan_frames[frame_idx]
        write_string(f"Статус кулера: [ {current_frame} ] ACTIVE", 5, 9, status_color | COLOR_BG_NAVY)
        
        for x in range(2, 78):
            local_memory_buffer[4 * SCREEN_WIDTH + x].Attributes |= 0x0100 # Линия над символом
            local_memory_buffer[12 * SCREEN_WIDTH + x].Attributes |= 0x0100 # Линия над символом

        frame_idx = (frame_idx + 1) % len(fan_frames)

        kernel32.WriteConsoleOutputW(
            h_back_buffer,
            ctypes.byref(local_memory_buffer),
            buffer_size_coord,
            buffer_coord,
            ctypes.byref(write_region)
        )
        
        time.sleep(0.05)

finally:
    kernel32.SetConsoleActiveScreenBuffer(h_original_out)
    kernel32.CloseHandle(h_back_buffer)
    print("n[СИСТЕМА] Оригинальный буфер экрана восстановлен. Ресурсы ядра очищены.")
