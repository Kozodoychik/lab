section .text
global _start

_start:
	mov rax, 41
	mov rdi, 2
	mov rsi, 1
	mov rdx, 0
	syscall

	mov r12, rax

	mov rax, 42
	mov rdi, r12
	mov rsi, sockaddr_in
	mov rdx, sockaddr_len
	syscall

	mov rax, 1
	mov rdi, r12
	mov rsi, msg
	mov rdx, msg_len
	syscall

	mov rax, 60
	xor rdi, rdi
	syscall

section .data
sockaddr_in:
	dw 2
	dw 0x901f
	dd 0x0100007f
	dq 0
sockaddr_len equ $ - sockaddr_in

msg: db "Hello from clean NASM assembly code!", 0x0a
msg_len equ $ - msg