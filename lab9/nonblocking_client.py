import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[КЛИЕНТ] Пауза перед подключением (сервер в это время крутит цикл)...")
time.sleep(3)

client_socket.connect(('127.0.0.1', 9995))
print("[КЛИЕНТ] Подключено. Пауза перед отправкой текста...")
time.sleep(3)

client_socket.send("Hello from non-blocking test".encode('utf-8'))
client_socket.close()