import win32gui
import win32con
import sys

WM_MY_COMMAND = win32con.WM_USER + 1337

print("[ОТПРАВИТЕЛЬ] Ищем окно приемника по зарегистрированному имени класса...")

hwnd = win32gui.FindWindow("SysProgHiddenReceiverClass18ProMaxChickenMcNugget", None)

if hwnd == 0:
	print("[ОШИБКА] Окно приемника не найдено в системе! Запустите сначала win_receiver.py.")
	sys.exit(1)

print(f"[ОТПРАВИТЕЛЬ] Цель найдена. HWND приемника: {hwnd}")
print("[ОТПРАВИТЕЛЬ] Вызываем PostMessage: отправляем асинхронный сигнал 777...")

win32gui.SendMessage(hwnd, WM_MY_COMMAND, 777, 0)