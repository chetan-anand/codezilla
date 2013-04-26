import sys
nod={}
opcode=[]
xy= open('xyz','r')
for row in xy:
	codes=row.split()
	nod[codes[0]]=[codes[0], codes[1]]
xy.close()
xy= open('opcode','r')
for row in xy:
	codes=row.split()
	opcode.append(codes[0])
xy.close()

for entry in sys.argv[1:]:
	flag=0
	init=open(entry,'r')
	for row in init:
		if row=="\n":
			continue
		codes=row.split()
		if codes[0]=='GLOBAL':
			continue
		if codes[0]=='EXTERN':
			continue
		if codes[0][0]==';':
			continue
		if codes[0][len(codes[0])-1]==':':
			continue
		if codes[0] in opcode:
			print codes[0]+" is in opcode list"
			continue
		else:
			print codes[0]+" is not in opcode list"
			flag==1
	if flag==1:
		print "The given file"+ entry +" has opcode errors"
	else:
		print "The given file"+ entry +" has no opcode errors"

