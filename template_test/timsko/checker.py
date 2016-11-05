import sys

sol = open(sys.argv[2], 'r')
ans = open(sys.argv[1], 'r')
sol = sol.readlines()
ans = ans.readlines()
for i in range(len(sol)):
	sol_line = sol[i].strip().split()
	ans_line = ans[i].strip().split()
	for j in range(len(sol_line)):
		if sol_line[j] != ans_line[j]:
			print "False"
			exit(0)

print "True"

