@1
D=M
@3
M=D        // M[3]=M[1]

@2
M=0        // M[2]=0

(LOOP)
@3
D=M       // D=M[3]
@END
D; JEQ    // If M[3]==0 goto END

@0
D = M
@2
M = M + D  // M[2]+=M[0]

@3
M = M - 1  // M[3]=M[3]-1

@LOOP
0;JMP

(END)
	@END
	0; JMP