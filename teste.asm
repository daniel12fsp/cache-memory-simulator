.data
string:	.asciiz "Hello World!(default Haha)"
entrada:	.asciiz "Dígite um inteiro para os loops:"
saida:	.asciiz "Número digitado:"

.text

main:
#-------(Start main)------------------------------------------------
	j teste

imprimir:
	la $a0, string		# Carrega endereço de string
	addi $v0, $zero, 4	# Imprime string
	syscall

	la $a0, entrada		# Carrega endereço de entrada
	addi $v0, $zero, 4	# Imprime entrada
	syscall

	addi $v0, $zero, 5	# Lê Inteiro
	syscall
	move $t0, $v0

	la $a0, saida		# Carrega endereço de saida
	addi $v0, $zero, 4	# Imprime saida
	syscall

	move $a0, $t0		# Carrega Inteiro para imprimir
	addi $v0, $zero, 1	# Imprime
	syscall
	
	jal atenum
	j sair

teste:
	addi $s0, $zero, 5 	# $s0 = 5
	move $s1, $s0 		# $s1 = 5
	add $s2, $s0, $s1 	# $s2 = 10
	sub $s3, $s0, $s2 	# $s3 = -5
	subi $s4, $s3, -8 	# $s4 = 3
	mul	$s5, $s3, $s4	# $s5 = -15
	div	$s6, $s2, $s4	# $s6 = 3
	slt $at, $zero, $s0 # $at = 1
	slti $s7, $s2, 2	# $s7 = 0
	
	j imprimir

sair:
	addi $v0, $zero, 10	# Sair
	syscall


atezero:
	move $a0, $t1		# Carrega Inteiro para imprimir
	addi $v0, $zero, 1	# Imprime
	syscall
	subi $t1, $t1, 1	# $t1 --

	slt $t2, $t1, $zero
	beq $t2, $zero, atezero
	jr $ra

atenum:
	move $a0, $t1		# Carrega Inteiro para imprimir
	addi $v0, $zero, 1	# Imprime
	syscall
	addi $t1, $t1, 1	# $t1 ++

	bne $t1, $t0, atenum
	j atezero
