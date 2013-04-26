'''
	Author: Chetan Anand and Abhinav Bommireddi
	Project: Assembler(Pass 1 and part of Pass 2)
	Date: 30.03.2013
	Version: 1.0
'''
import sys
#################################################storing information from the opcode file ##############################################
ptr = open('opcode', 'r')

mnemonic={}
opcode={}

for row in ptr:

	codes=row.split()
	mnemonic[codes[0]]=[int(codes[2])]
	opcode[codes[0]]=codes[1]
ptr.close()
print mnemonic
print opcode


#######################################################################################################################################
##############           Opening and reading from the assembly source file created after file conversion      ###############
totarg=len(sys.argv)-1
globvar={}
gvar=[]
gp=[]
gpl={}
size={}
externvar={}
for entry in sys.argv[1:]:
	source = open(entry,'r')
	labeltable={}
	labels=[]
	#optable={}
	#keywords=[]
	#instruction=[]
	#line={}
	addcnt=0
	cnt=0
	for row in source:
		if row=="\n":
			continue
		codes=row.split()
		if codes[0][0]!=';':
			if codes[0][len(codes[0])-1]==':':
				if codes[1]=='equ':
					labels.append(codes[0][:-1])
					labeltable[codes[0][:-1]]=[codes[0][:-1], addcnt]
					addcnt= addcnt + 1
				elif codes[1]=='ds':
					labels.append(codes[0][:-1])
					labeltable[codes[0][:-1]]=[codes[0][:-1], addcnt]
					addcnt = addcnt + int(codes[2])
				elif codes[1]=='db':
					labels.append(codes[0][:-1])
					labeltable[codes[0][:-1]]=[codes[0][:-1], addcnt]
					for word in codes:
						if word[len(word)-1]==',':
							addcnt = addcnt+1
					addcnt= addcnt+1
				else:
					print codes[0], addcnt
					#keywords.append(codes[0])
					labels.append(codes[0][:-1])
					labeltable[codes[0][:-1]]=[codes[0][:-1], addcnt]
					print codes[1], addcnt, opcode[codes[1]]
					#keywords.append(codes[1])
					#instruction.append(codes[1])
					#optable[codes[1]]=[codes[1], addcnt, opcode[codes[1]]]
					addcnt=addcnt + int(mnemonic[codes[1]][0])
			elif codes[0]=='GLOBAL':
				path = "/home/codefire/assembler/"+entry
				globvar[codes[1]]=[codes[1], path, addcnt]
				gpl[path]=[path, addcnt]
				gp.append(path)
				gvar.append(codes[1])
				#labels.append(codes[1])
				#labeltable[codes[1]]=[codes[1], addcnt]
				if codes[2]=='equ':
					addcnt= addcnt + 1
				elif codes[2]=='ds':
					addcnt = addcnt + int(codes[3])
				elif codes[2]=='db':
					for word in codes:
						if word[len(word)-1]==',':
							addcnt = addcnt+1
					addcnt= addcnt+1
			elif codes[0]=='EXTERN':
				fname = "externtable_" + entry
				ext = open(fname,'w+')
				ext.write(" "+ codes[1]+" ")
				ext.close()
				#externvar[codes[1]]=[codes[1]]
				continue
			else:
				print codes[0], addcnt, opcode[codes[0]]
				#keywords.append(codes[0])
				#instruction.append(codes[0])
				#optable[codes[0]]=[codes[0], addcnt, opcode[codes[0]]]
				addcnt=addcnt + int(mnemonic[codes[0]][0])

	source.close()
	size[entry]=[entry, addcnt]

	#print line
	'''print keywords
	print instruction
	print optable'''

	#print labeltable

	'''keyword = open('keywords.txt','w+')
	for row in keywords:
		keyword.write(row + "\n")
	keyword.close()

	instruct = open('instructions.txt','w+')
	for row in instruction:
		instruct.write(row + "\n")
	instruct.close()
	
	optab = open('opcodetable.txt','w+')
	for row in optable:
		optab.write(optable[row][0]+"	"+str(optable[row][1])+"	"+optable[row][2]+"\n")
	optab.close()'''
	###################################################################
	fname = "label_" + entry
	label = open(fname,'w+')
	for row in labels:
		label.write(row + "\n")
	label.close()


	fname = "labeltable_" + entry
	labeltab = open(fname,'w+')
	for row in labeltable:
		labeltab.write(labeltable[row][0]+"	"+str(labeltable[row][1])+"\n")
	labeltab.close()
	
	'''fname = "localvar_"+entry
	lvar = open(fname,'w+')
	for row in  localvar:
		lvar.write(localvar[row][0]+"	"+str(localvar[row][1])+"\n")'''
####################   pass-2 ###############################################################################################
	fname= "modified_"+ entry 
	source = open(entry,'r')
	modify = open(fname,'w+')
	for row in source:
		codes=row.split()
		if row=="\n" or codes[0][0]==';':
			continue
		for code in codes:
			if code in labels:
				modify.write(" $"+str(labeltable[code][1])+" ")
				continue
			if code[len(code)-2]=='+':
				y=code[:-2]
				modify.write(" $"+str(labeltable[y][1]+int(code[len(code)-1]))+" ")
				continue
			y=code[:-1]
			if y in labels:
			#modify.write(" "+str(labeltable[y][1])+": ")
				continue 
			else:
				modify.write(" "+code+" ")
		modify.write("\n")	
	modify.close()
	source.close()

##############################################################################################################################
print globvar
print gvar
print size
##################################################   After linking ##############################################################
for entry in sys.argv[1:]:
	fname= "modified_"+entry
	oname= "output_"+entry 
	source = open(fname,'r')
	modify = open(oname,'w+')
	for row in source:
		codes=row.split()
		if row=="\n" or codes[0][0]==';':
			continue
		for code in codes:
			if codes[0]=='GLOBAL' or codes[0]=='EXTERN':
				modify.write(" "+code+" ")
				continue
			if code in gvar:
				modify.write(" "+globvar[code][1]+"$"+str(globvar[code][2])+" ")
				#modify.write(" "+str(labeltable[y][1])+": "
				continue
			else:
				modify.write(" "+code+" ")
		modify.write("\n")	
	modify.close()
	source.close()
	
####################################################	Loading Part #############################################################
load={}
flag=1
	
for entry in sys.argv[1:]:
	x=int(raw_input("Please Enter the loading address of "+entry+" = "))
	path='/home/codefire/assembler/'+entry
	load[path]=[path, x]	
print load
if flag==1:
	ld=open('loader.txt','w+')
	for entry in sys.argv[1:]:
		oname= "output_"+entry
		path='/home/codefire/assembler/'+entry
		source = open(oname,'r')
		for row in source:
			codes=row.split()
			if row=="\n" or codes[0][0]==';':
				continue
			for code in codes:
				if code[0]=='$':
					y=code[1:]
					ld.write(" "+str(int(y)+int(load[path][1]))+" ")
					continue
				ld.write(" "+code+" ")
			ld.write("\n")	
		source.close()
	ld.close()
	ld=open('loader.txt','r')
	last=open('last_output','w+')
	for row in ld:
		codes=row.split()
		for code in codes:
			if code=='GLOBAL':
				continue
			if code=='EXTERN':
				continue
			tag=code.split('$')
			z=tag[0]
			#p=int(tag[1])
			if  z in gp:
				last.write(" "+str(load[z][1]+gpl[z][1])+" ")
			else:
				last.write(" "+code+" ")
		last.write("\n")
	last.close()
	ld.close()
