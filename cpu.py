import subprocess
import os
import sys
import time

if len(sys.argv) == 1:
	print 'need input pid'
	exit(-1)

pid=None

interval = 1


filterThread = False
filterThreadName = ''
loop = -1
for x in sys.argv:
	loop += 1
	if x == '-name':
		if len(sys.argv) < (loop + 2):
			print '-name has no param'
			exit(-1)
		filterThread = True
		filterThreadName = sys.argv[loop + 1]
	if x == '-p':
		if len(sys.argv) < (loop + 2):
			print '-p has no param'
			exit(-1)
		pid = str(sys.argv[loop + 1])
	if x == '-t':
		if len(sys.argv) < (loop + 2):
			print '-t has no param'
			exit(-1)
		interval = float(sys.argv[2])

if pid == None:
	print 'pid not input, python cpu.py -p 1342'
	exit(-1)




file='%s.js' % pid
if not os.path.exists(file):
	print 'no stack file, we try to make stack file'
	cmd = 'jstack %s > %s.js' % (pid,pid)
	subprocess.Popen([cmd],stdout=subprocess.PIPE,shell=True).communicate()

script="cat %s.js |grep tid|awk -F 'nid=' '{print $2}'|awk '{print $1}'" % pid
output = subprocess.Popen([script],stdout=subprocess.PIPE,shell=True).communicate()
threadId=output[0].split('\n')[:-1]


script="cat %s.js |grep tid|awk -F '\"' '{print $2}'" % pid
output = subprocess.Popen([script],stdout=subprocess.PIPE,shell=True).communicate()
threadName=output[0].split('\n')[:-1]


def show():
	script="top -H -p %s -n 1|grep java" % pid
	output = subprocess.Popen([script],stdout=subprocess.PIPE,shell=True).communicate()
	topInfoArray=output[0].split('\n')
	topInfoArray.remove('')

	tidOrigin = []
	cpu = []
	tid = []
	for x in topInfoArray:
		line = x.strip().split(' ')
		count = line.count('')
		for i in range(count):
			line.remove('')
		cpuIndex = line.index('java')-3
		tidIndex = line.index('fenbi')-1
		tidOrigin.append(line[tidIndex])
		tid.append(hex(int(line[tidIndex].split('m')[-1])))
		cpu.append(line[cpuIndex])


	print "pid   cpu   threadName"
	loop = -1
	for x in tid:
		loop += 1
		if x not in threadId:
			continue
		index = threadId.index(x)
		if filterThread and filterThreadName not in threadName[index]:
			continue
		print tidOrigin[loop]," ",cpu[loop]," ",threadName[index]



while True:
	os.system('clear')
	show()
	time.sleep(interval)




