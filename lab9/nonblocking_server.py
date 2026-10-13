import socket
import time
import os

PORT = 9995

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', PORT))
server_socket.listen(1)

server_socket.setblocking(False)

print(f"[НЕБЛОКИРУЮЩИЙ СЕРВЕР] Инициализирован. PID: {os.getpid()}")
print("[СЕРВЕР] Начинаем безумный цикл опроса (Polling) в Ring 3...")

client_socket = None

while True:
	try:
		client_socket, client_address = server_socket.accept()
		print(f"\n[СЕРВЕР] Ура! Подключение перехвачено: {client_address}")
		break
	except BlockingIOError as e:
		print(".", end="", flush=True)
		#time.sleep(0.01)

client_socket.setblocking(False)

print("[СЕРВЕР] Переходим к неблокирующему чтению данных...")
while True:
	try:
		data = client_socket.recv(1024)
		if data:
			print(f"\n[СЕРВЕР] Байты считаны из RX-буфера: {data.decode('utf-8')}")
			break
	except BlockingIOError:
		print("*", end="", flush=True)
		time.sleep(0.01)

client_socket.close()
server_socket.close()
print("\n[СЕРВЕР] Работа завершена.")