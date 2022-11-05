(LOOP)
	// SET Index
	@SCREEN
	D=A
	@8192
	D=D+A
	@i
	M=D

	// choise color
	@KBD
	D=M
	@prev
	M=D

	@BLACK
	D; JGT
	@WHITE
	0; JMP
	
(WHITE)
	@color
	M=0
	@FILL
	0;JMP
(BLACK)	
	@color
	M=-1
(FILL)
	// if prev != now-key goto loop
	@prev
	D=M
	@KBD
	D=D-M
	@LOOP
	D; JNE

	// i = i -1
	@i
	D=M-1
	M=D
	// if i < 0 goto LOOP
	@LOOP
	D; JLT
	
	// M[CURRENT_SCREEN_ADDRESS] = color
	@color
	D=M
	@i
	A=M
	M=D
	@FILL
	0; JMP
	
