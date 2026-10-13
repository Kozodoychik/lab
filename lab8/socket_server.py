import socket
import os

PORT = 9999

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"[СЕРВЕР] Инициализация. Мой PID: {os.getpid()}")
serv_socket.bind(('127.0.0.1', PORT))
serv_socket.listen(1)
print(f"[СЕРВЕР] Сокет переведен в режим listen. Порт {PORT} зарезервирован в ядре.")

print("[СЕРВЕР] Вызов accept(). Поток сейчас уйдет в глубокий сон...")
client_socket, client_address = serv_socket.accept()
print(f"[СЕРВЕР] Поток разбужен! Зафиксировано подключение от {client_address}")

print("[СЕРВЕР] Ожидание данных от клиента (вызов recv)...")
data = client_socket.recv(1024)
print(f"[СЕРВЕР] Данные получены из RX-буфера ядра: {data.decode('utf-8')}")

print("[СЕРВЕР] Закрываем соединение и освобождаем дескрипторы.")
client_socket.close()
#serv_socket.close()