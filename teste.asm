main:
#-------(Start main)------------------------------------------------
	
	addi $s0, $zero, 5 	# $s0 = 5
	move $s1, $s0 		# $s1 = 5
	add $s2, $s0, $s1 	# $s2 = 10
	sub $s3, $s0, $s2 	# $s3 = -5
	subi $s4, $s3, -8 	# $s4 = 3
	mul	$s5, $s3, $s4	# $s5 = -15
	div	$s6, $s2, $s4	# $s6 = 3
	slt $at, $zero, $s0 # $at = 1
	slti $s7, $s2, 2	# $s7 = 0
