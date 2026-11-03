section .data
msg_start db "Текущий адрес границы кучи: 0x", 0
msg_len equ $ - msg_start

msg_success db 0xa, "Память успешно выделена. Записываем данные...", 0xa, 0
msg_success_len equ $ - msg_success

msg_done db 0xa, "Память успешно возвращена ядру Linux.", 0xa, 0
msg_done_len equ $ - msg_done

test_str db "Привет от студентов колледжа! Память работает.", 0xa, 0
test_str_len equ $ - test_str

section .bss
initial_brk resq 1
new_brk     resq 1
buffer      resb 16

section .text
global _start

_start:
	mov rax, 12
	mov rdi, 0
	syscall

	mov [initial_brk], rax

	mov rax, 1
	mov rdi, 1
	mov rsi, msg_start
	mov rdx, msg_len
	syscall

	mov rax, [initial_brk]
	call print_hex

	mov rax, 12
	mov rdi, [initial_brk]
	add rdi, 4096
	syscall
	mov [new_brk], rax

	cmp rax, [initial_brk]
	je .exit_error

	mov rax, 1
	mov rdi, 1
	mov rsi, msg_success
	mov rdx, msg_success_len
	syscall

	mov rsi, test_str
	mov rdi, [initial_brk]
	mov rcx, test_str_len
	cld
	rep movsb

	mov rax, 1
	mov rdi, 1
	mov rsi, [initial_brk]
	mov rdx, test_str_len
	syscall

	; Вызываем segfault
	mov rax, 0xff
	mov rdi, [new_brk]
	add rdi, 10
	mov [rdi], rax

	mov rax, 12
	mov rdi, [initial_brk]
	syscall

	mov rax, 1
	mov rdi, 1
	mov rsi, msg_done
	mov rdx, msg_done_len
	syscall

	mov rax, 60
	mov rdi, 0
	syscall

	.exit_error:
		mov rax, 60
		mov rdi, 1
		syscall

print_hex:
    mov rcx, 16
    mov rbx, buffer
	.loop:
    	rol rax, 4
    	mov dl, al
    	and dl, 0x0F
    	add dl, '0'
    	cmp dl, '9'
    	jbe .store
    	add dl, 7
	.store:
    	mov [rbx], dl
    	inc rbx
    	loop .loop

    	mov rax, 1
    	mov rdi, 1
    	mov rsi, buffer
    	mov rdx, 16
    	syscall
    	ret

