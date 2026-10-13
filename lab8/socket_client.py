import socket
import time

PORT = 9999

print("[КЛИЕНТ] Создаем сокет...")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("[КЛИЕНТ] Пауза 3 секунды перед подключением...")
time.sleep(3)

print("[КЛИЕНТ] Инициируем TCP Handshake (вызов connect)...")
client_socket.connect(('127.0.0.1', PORT))
print("[КЛИЕНТ] Соединение установлено. Пауза 3 секунды перед отправкой данных...")
time.sleep(3)

print("[КЛИЕНТ] Отправляем данные в TX-буфер ядра...")
client_socket.send("Test payload".encode('utf-8'))

client_socket.close()
print("[КЛИЕНТ] Сокет закрыт.")