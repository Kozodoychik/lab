section .data
    clear_cmd     db 0x1B, "[2J"
    clear_len     equ $ - clear_cmd

    color_green_blue db 0x1B, "[32;44m"
    color_len1       equ $ - color_green_blue

    color_red_black  db 0x1B, "[31;40m"
    color_len2       equ $ - color_red_black

    reset_color   db 0x1B, "[0m"
    reset_len     equ $ - reset_color

    cursor_pos1   db 0x1B, "[5;20H"
    cursor_len1   equ $ - cursor_pos1

    cursor_pos2   db 0x1B, "[10;10H"
    cursor_len2   equ $ - cursor_pos2

    msg1 db "=== SYSTEM PROGRAMMING TERMINAL BUFFER ==="
    msg1_len equ $ - msg1

    msg2 db "CRITICAL MONITOR: ACTIVE"
    msg2_len equ $ - msg2

	exit_pos db 0x1B, "[15;1H"
    exit_pos_len equ $ - exit_pos

section .text
    global _start

_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, clear_cmd
    mov rdx, clear_len
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, cursor_pos1
    mov rdx, cursor_len1
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, color_green_blue
    mov rdx, color_len1
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, msg1
    mov rdx, msg1_len
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, cursor_pos2
    mov rdx, cursor_len2
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, color_red_black
    mov rdx, color_len2
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, msg2
    mov rdx, msg2_len
    syscall

    ;mov rax, 1
    ;mov rdi, 1
    ;mov rsi, reset_color
    ;mov rdx, reset_len
    ;syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, exit_pos
    mov rdx, exit_pos_len
    syscall

    
    mov rax, 60
    xor rdi, rdi
    syscall