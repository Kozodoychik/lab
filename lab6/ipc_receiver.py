import posix_ipc
import sys

QUEUE_NAME = "/sys_prog_queue"

try:
	mq = posix_ipc.MessageQueue(QUEUE_NAME, flags=posix_ipc.O_CREAT)
except posix_ipc.ExistentialError:
	print("[ОШИБКА] Очередь не найдена в ядре. Сначала запустите ipc_sender.py")
	sys.exit(1)

print("[ПРИЁМНИК] Успешно подключено к системной очереди. Начинаем чтение...")

while True:
	bin_data, priority = mq.receive()
	message = bin_data.decode("utf-8")

	print(f"[ПРИЁМНИК] Получено из ядра: '{message}'")

	if "5" in message:
		print("[ПРИЁМНИК] Получено последнее сообщение.")
		break

mq.close()
posix_ipc.unlink_message_queue(QUEUE_NAME)
print("[ПРИЁМНИК] Очередь удалена из операционной системы.")
