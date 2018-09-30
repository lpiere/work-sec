v = [1]
n = 5
for i in range(1, n+1):
	print(v)
	newLen = len(v)+1
	a = []
	for j in range(0, newLen):
		if(j != 0 and j!= newLen-1):
			a.append(v[j]+v[j-1])
		else:
			a.append(1)
	
	v = a[:] 
	
