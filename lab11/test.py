import ctypes
import os

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

kernel32.LoadLibraryW.argtypes = [ctypes.c_wchar_p]
kernel32.LoadLibraryW.restype = ctypes.c_void_p

kernel32.GetProcAddress.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p
]
kernel32.GetProcAddress.restype = ctypes.c_void_p

kernel32.FreeLibrary.argtypes = [ctypes.c_void_p]
kernel32.FreeLibrary.restype = ctypes.c_int

print(f"PID процесса: {os.getpid()}")

h_module = kernel32.LoadLibraryW("user32.dll")
if not h_module:
    raise ctypes.WinError(ctypes.get_last_error())

try:
    address = kernel32.GetProcAddress(
        h_module,
        b"MessageBoxW"
    )

    if not address:
        raise ctypes.WinError(ctypes.get_last_error())

    print(f"Базовый адрес user32.dll: 0x{h_module:016X}")
    print(f"Адрес MessageBoxW:        0x{address:016X}")
    print(f"Смещение функции:         0x{address - h_module:X}")
finally:
    kernel32.FreeLibrary(h_module)