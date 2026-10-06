import posix_ipc
import time

QUEUE_NAME = "/sys_prog_queue"

print("[ОТПРАВИТЕЛЬ] Обращаемся к ядру для создания очереди...")

mq = posix_ipc.MessageQueue(QUEUE_NAME, flags=posix_ipc.O_CREAT, mode=0o666)

print(f"[ОТПРАВИТЕЛЬ] Системная очередь {QUEUE_NAME} успешно инициализирована.")

for i in range(1, 6):
	message = f"Message ID {i} payload"
	bin_data = message.encode("utf-8")
	print(f"[ОТПРАВИТЕЛЬ] Выполняем mq_send: отправка '{message}' в буфер ядра...")
	mq.send(bin_data)
	time.sleep(0.5)
print("[ОТПРАВИТЕЛЬ] Все сообщения отправлены в Ring 0. Завершение работы")
mq.close()
