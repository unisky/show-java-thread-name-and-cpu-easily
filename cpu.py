import subprocess
import os
import sys
import time

if len(sys.argv) == 1:
	print 'need input pid'
	exit(-1)

pid=str(sys.argv[1])


file='%s.js' % pid
if not os.path.exists(file):
	print 'no stack file, we try to make stack file'
	cmd = 'jstack %s > %s.js' % (pid,pid)
	subprocess.Popen([cmd],stdout=subprocess.PIPE,shell=True).communicate()


def show():
	script="top -H -p %s -n 1|grep fenbi|awk '{print $1\" \"$9}'" % pid
	output = subprocess.Popen([script],stdout=subprocess.PIPE,shell=True).communicate()
	cpu=output[0].split('\n')[:-1]
	tid = [hex(int(x.split(' ')[0].split('m')[-1])) for x in cpu]


	script="cat %s.js |grep tid|awk -F 'nid=' '{print $2}'|awk '{print $1}'" % pid
	output = subprocess.Popen([script],stdout=subprocess.PIPE,shell=True).communicate()
	threadId=output[0].split('\n')[:-1]


	script="cat %s.js |grep tid|awk -F '\"' '{print $2}'" % pid
	output = subprocess.Popen([script],stdout=subprocess.PIPE,shell=True).communicate()
	threadName=output[0].split('\n')[:-1]

	print "pid   cpu   threadName"
	loop = -1
	for x in tid:
		loop += 1
		if x not in threadId:
			continue
		index = threadId.index(x)
		print cpu[loop]," ",threadName[index]

interval = 1
if len(sys.argv) >= 3:
	interval = float(sys.argv[2])
print interval
while True:
	os.system('clear')
	show()
	time.sleep(interval)



