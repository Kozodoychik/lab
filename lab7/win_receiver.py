import win32gui
import win32con
import win32process
import os

WM_MY_COMMAND = win32con.WM_USER + 1337

def window_procedure(hwnd, msg, wparam, lparam):
	if msg == WM_MY_COMMAND:
		print(f"\n[ПРИЕМНИК] Перехвачено системное сообщение WM_USER+1337!")
		print(f"[ПРИЕМНИК] Параметр команды (WPARAM): {wparam}")
		if wparam == 777:
			print("[ПРИЕМНИК] Сигнал подтвержден. Выполняем экстренное завершение процесса...")
			os._exit(0)
			return 0
	return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

wc = win32gui.WNDCLASS()
wc.lpfnWndProc = window_procedure
wc.lpszClassName = "SysProgHiddenReceiverClass18ProMaxChickenMcNugget"
class_atom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(class_atom, "SysProgReceiverWindow18ProMaxChickenMcNugget", 0, 0, 0, 0, 0, 0, 0, 0, None)

print(f"[ПРИЕМНИК] Процесс запущен. Мой PID: {os.getpid()}")
print(f"[ПРИЕМНИК] Ядро Windows выделило нам дескриптор HWND: {hwnd}")
print("[ПРИЕМНИК] Входим в бесконечный системный цикл выборки сообщений GetMessage()...")

win32gui.PumpMessages()