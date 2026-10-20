section .data

encryption_key: db 0x5a

section .text
global asm_encrypt

asm_encrypt:
	cmp rsi, 0
	jle .done

	xor rcx, rcx
	.loop:
		mov al, [rel encryption_key]

		xor byte [rdi + rcx], al

		inc rcx
		cmp rcx, rsi
		jl .loop
	.done:
	ret