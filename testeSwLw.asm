.data
string:	.asciiz "Hello World!(default Haha)"
vetor:	.word 320 90 1 4 5 84 62 10 2 36
string_vetor:	.asciiz "Vetor:"

.text

main:
#-------(Start main)------------------------------------------------
	addi $t0, $zero, 10			# $t0 = 10
	la $t1, vetor				# $t1 = end. vetor

	la $a0, string_vetor
	addi $v0, $zero, 4			# Imprime valor vetor[$t1]
	syscall

imprimir:

	lw $a0, ($t1)				# $a0 = valor vetor[$t1]
	addi $v0, $zero, 1			# Imprime valor vetor[$t1]
	syscall

	subi $t0, $t0, 1			# $t0 --
	addi $t1, $t1, 4			# $t1 += 4

	slt $t2, $zero, $t0			# True if($zero < $t0)
	bne $t2, $zero, imprimir	#

	#fim_imprimir:

	addi $t0, $zero, 10			# $t0 = 10
	la $t1, vetor				# $t1 = end. vetor

modificar:

	sw $t0, ($t1)				# $a0 = valor vetor[$t1]
	move $a0, $t0	
	addi $v0, $zero, 1			# Imprime valor vetor[$t1]
	syscall

	subi $t0, $t0, 1			# $t0 --
	addi $t1, $t1, 4			# $t1 += 4

	slt $t2, $zero, $t0			# True if($zero < $t0)
	bne $t2, $zero, modificar	#

