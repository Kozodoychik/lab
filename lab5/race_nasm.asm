section .data
global shared_counter
shared_counter: dq 0

section .text
global thread_function
global main		; Иначе не слинкуется

thread_function:
	mov rcx, 10000000
	.loop:
		mov rax, [shared_counter]
		inc rax
		mov [shared_counter], rax
		loop .loop

	xor rax, rax
	ret

main:
	mov rax, 60
	mov rdi, 0
	syscall
