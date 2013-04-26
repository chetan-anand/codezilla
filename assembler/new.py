import sys
tot= len(sys.argv)
cmd = str(sys.argv)
print sys.argv[1]
print tot
for row in sys.argv[1:]:
	fname="modified_"+row
	print fname
