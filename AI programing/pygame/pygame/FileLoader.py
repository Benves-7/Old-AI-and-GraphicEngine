def LoadFiletoList(fileName):
	f = open(fileName, "r")
	t = f.read().splitlines()
	f.close()
	print("load done.")
	return t

def LoadFile(fileName):
	return open(fileName, r) 
