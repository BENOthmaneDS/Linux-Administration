import sys,re,os


def help():
	return " Syntaxe error\n" + sys.argv[0] + " nbDisk size [FS]"


def checkParam():
	if len(sys.argv) < 3 or len(sys.argv) > 4:
		print(help())
		sys.exit(0)
	if not (sys.argv[1]).isdigit():
		print(help())
		sys.exit(1)
	if not (re.match('^[0-9]+(K|M|G)$', sys.argv[2])):
		print("Expected (K|M|G) as the size type")
		sys.exit(2)
	if len(sys.argv) == 4:
		if not (sys.argv[3] in ["ext2","ext3","ext4"]):
			print("Wrong File System (ext2|ext3|ext4)")
			sys.exit(3)

def normalizedSpace(size):
	unit = size[-1]
	space = float(size[0:len(size)-1])
	if unit == 'M':
		space = space * 10**3
	if unit == 'G':
		space = space * 10**6
	return space

def checkSpace():
	requiredSpace = normalizedSpace(sys.argv[2]) * int(sys.argv[1])
	df = os.popen("df -h| grep /home")
	results = df.read()
	df.close()
	if len(results) == 0:
		df = os.popen("df -h| grep /$")
		results = df.read()
		df.close()
	availableSpace = normalizedSpace(results.split()[3])
	if requiredSpace + 10**5 > availableSpace :
		print("Low Disk Space")

def checkLoops():
	occupedLoops = []
	lo = os.popen("losetup -a")
	for l in lo.readlines():
		occupedLoops.append(l[len('/dev/loop'):l.index(':')])
	lo.close()
	allLoops = []
	lo = os.popen('ls /dev/loop*')
	allLoops = [loop[len('/dev/loop'):len(loop) - 1] for loop in lo.readlines() if not(loop.endswith('-control\n'))]
	index = len(allLoops)
	for loop in occupedLoops:
		allLoops.remove(loop)

	if len(allLoops) >= int(sys.argv[1]):
		return allLoops
	else:
		for i in range(int(sys.argv[1]) - len(allLoops)):
			os.popen("mknod /dev/loop" + str(index + i) + " b 7 " + str(index + i))
			allLoops.append(str(index + i))
		return allLoops

def createDisks():
	checkParam()
	checkSpace()
	nbDisks = int(sys.argv[1])
	size = int(normalizedSpace(sys.argv[2])) * 1000 #We used K as unit
	#get all available loops
	loops = checkLoops()
	for i in range(nbDisks):
		os.system('dd if=/dev/zero of=disk' + loops[i] + ' bs=' + str(size) + ' count=1')
		os.system('losetup /dev/loop' + loops[i] + ' disk' + loops[i])


createDisks()
